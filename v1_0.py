import pygame as pg, math, random

pg.init()


window_size = [720,720]
window = pg.display.set_mode(window_size)
canvas = pg.Surface(window_size,pg.SRCALPHA)
font = pg.font.SysFont(None, 20) 

node_count = 1 # keeping the count of how long the body is, We atleast have head so hence 1
selected_node = 0#which node's info is being displayed?
p_head = [[0, 15], [2, 11], [3, 8], [3, 4], [6, 4], [10, 7], [10, -3], [6, -11], [2, -15], [-2, -15], [-6, -11], [-10, -3], [-10, 7], [-6, 4], [-3, 4], [-3, 8], [-2, 11]]
p_leye = [[-2, -8], [-4, -7], [-5, -5], [-5, -3], [-2, -5]]
p_reye = [[2, -8], [4, -7], [5, -5], [5, -3], [2, -5]]
p_body = [[0,-14],[4,-12],[7,-9],[5,-7],[5,-5],[8,-2],[10,2],[10,6],[6,1],[4,1],[2,7],[0,14],[-2,7],[-4,1],[-6,1],[-10,6],[-10,2],[-8,-2],[-5,-5],[-5,-7],[-7,-9],[-4,-12]]
p_wing =[[0, -10], [-3, -7], [-1, -5], [-1, -3], [-4, -3], [-13, -13], [-16, -14], [-20, -12], [-24, -9], [-28, -4], [-30, 1], [-23, -6], [-19, -9], [-15, -11], [-14, -10], [-16, -8], [-20, -4], [-23, 1], [-23, 3], [-21, 0], [-18, -4], [-14, -7], [-12, -8], [-12, -6], [-15, -2], [-17, 2], [-18, 5], [-18, 8], [-16, 4], [-13, -1], [-10, -5], [-9, -5], [-9, -3], [-12, 1], [-13, 4], [-13, 7], [-11, 10], [-12, 5], [-10, 1], [-9, 4], [-5, 10], [-7, 4], [-8, -1], [-6, -3], [0, 2], [6, -3], [8, -1], [7, 4],[5, 10], [9, 4], [10, 1], [12, 5], [11, 10], [13, 7], [13, 4], [12, 1], [9, -3], [9, -5], [10, -5], [13, -1], [16, 4], [18, 8], [18, 5], [17, 2], [15, -2],[12, -6], [12, -8], [14, -7], [18, -4], [21, 0], [23, 3], [23, 1], [20, -4], [16, -8], [14, -10], [15, -11], [19, -9], [23, -6], [30, 1], [28, -4], [24, -9], [20, -12], [16, -14], [13, -13], [4, -3], [1, -3], [1, -5], [3, -7]]



#we will use linked list to store the dragon's body, and its attributes and its functions


#defining class Node
class Node:
    def __init__(self,index,data):
        self.prev = None
        self.next = None
        self.index = index
        self.data = data
        self.angle = 0
        self.xpos = 0
        self.ypos = 0
        self.size = 0 # gets updated immidiately

    def __str__(self):
        return f"index:{self.index},data:{self.data},xpos:{self.xpos},ypos:{self.ypos}"
    
    def draw(self):
        color = int(220 - (self.index * (220 - 0) / max(1, node_count)))
        #head
        if self.prev == None:
            p_h = [[self.xpos + x, self.ypos + y] for x,y in [rotate_point(x*self.size, y*self.size, -self.angle) for x,y in p_head]]
            p_le = [[self.xpos + x, self.ypos + y] for x,y in [rotate_point(x*self.size, y*self.size, -self.angle) for x,y in p_leye]]
            p_re = [[self.xpos + x, self.ypos + y] for x,y in [rotate_point(x*self.size, y*self.size, -self.angle) for x,y in p_reye]]

            pg.draw.polygon(canvas,(max(68,color),max(68,color),max(78,color)),p_h)
            pg.draw.polygon(canvas,(0,0,0),p_le)
            pg.draw.polygon(canvas,(0,0,0),p_re)
            pg.draw.polygon(canvas,(53,53,62),p_h,3)


            
        else:
            #every 3rd body will be wings
            if self.index%3 == 0:
                p_w = [[self.xpos + x, self.ypos + y] for x,y in [rotate_point(x*self.size*2, y*self.size*2, -self.angle) for x,y in p_wing]]
                pg.draw.polygon(canvas,(max(68,color),max(68,color),max(78,color)),p_w)
                pg.draw.polygon(canvas,(53,53,62),p_w,3)
            else:
                p_b = [[self.xpos + x, self.ypos + y] for x,y in [rotate_point(x*self.size, y*self.size, -self.angle) for x,y in p_body]]
                pg.draw.polygon(canvas,(max(68,color),max(68,color),max(78,color)),p_b)
                pg.draw.polygon(canvas,(53,53,62),p_b,3)

        
        if self.index == selected_node:
            pg.draw.circle(canvas,(0,255,0),(self.xpos,self.ypos),self.size,3)

        text = font.render(str(self.data), True, (0,0,0))
        text_rect = text.get_rect(center=(self.xpos,self.ypos))

        # blit text onto *the same* canvas surface
        canvas.blit(text, text_rect)

    def update(self):
        #changing the size of the Node based on its position in the list-
        self.size = int(5 - (self.index * (5 - 2) / max(1, node_count)))

        # Smoothing factor (0 < alpha < 1, smaller = slower follow)
        alpha = 0.1  

        #getting mouse position if the node being called is the head and making the node follow mouse
        if self.prev == None:
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.xpos += (mouse_x-self.xpos) * alpha
            self.ypos += (mouse_y-self.ypos) * alpha

        #if not head, It will follow its previous node
        else:
            self.xpos += (self.prev.xpos - self.xpos) * alpha
            self.ypos += (self.prev.ypos - self.ypos) * alpha

        #if head
        if self.prev == None:
            mx,my = pg.mouse.get_pos()
            dx, dy = mx - self.xpos, my - self.ypos
            self.angle = math.degrees(math.atan2(-dy, dx)) -90
        else:
            mx,my = self.prev.xpos,self.prev.ypos
            dx, dy = mx - self.xpos, my - self.ypos
            self.angle = math.degrees(math.atan2(-dy, dx)) -90

        

head = Node(0,int(input("Enter data for the head:")))

def insert(data):
    global node_count, head
    rh = head
    #finding tail
    while rh.next != None:
        rh = rh.next
    #breaks out of loop when tail is found
    
    #adding node onto tail
    rh.next = Node(node_count,data)
    rh.next.prev = rh

    #setting the position of the new Node to be a x distance behidn the 2nd last node- 
    if rh.prev != None:
        rh.next.xpos = rh.xpos-(-1*(rh.prev.xpos-rh.xpos))#multiplying by -1 to change its direction
        rh.next.ypos = rh.ypos-(-1*(rh.prev.ypos-rh.ypos))
    # if prev == none ie node is head
    else:
        rh.next.xpos, rh.next.ypos = 0,0

    #incremening the count after adding said node
    node_count += 1 

def search(target):
    global head
    rh = head
    while rh.data != target:
        rh = rh.next

    if rh.data == target:
        print("found element at index->",rh.index)
    else:
        print("Element not found.")

    
def delete(target):
    global head, node_count
    rh = head
    print(rh)
    while rh.data != target:
        rh = rh.next

    if rh.data == target and node_count>1:
        #checking if node in between two other nodes or not
        if rh.prev != None and rh.next != None:
            #for normal case
            rh.prev.next = rh.next
            rh.next.prev = rh.prev
        # if element being deleted == head
        elif rh.prev == None:
            head.next.prev = None
            head = head.next
        #for tail
        else:
            rh.prev.next = None
        node_count-=1

        #reindexing the nodes
        rh = head
        for i in range(node_count):
            rh.index = i
            rh = rh.next

    else:
        print("Could not delete, Element not in list or is the last element.")

def rotate_point(px, py, angle_deg):
    rad = math.radians(angle_deg)
    x_new = px * math.cos(rad) - py * math.sin(rad)
    y_new = px * math.sin(rad) + py * math.cos(rad)
    return [x_new, y_new]

def display():
    global head
    rh = head
    
    while rh.next != None:
        print(rh,"->")
        rh = rh.next
    print(rh)

def show_menu():
    print("1.insert")
    print("2.search")
    print("3.print")
    print("4.delete")


def input_handler(inp:str):
    global selected_node

    if inp == "menu":
        show_menu()

    if inp == "insert" or inp == "1":
        x = int(input("Enter data for new node(int):"))
        insert(x)

    if inp == "search" or inp == "2":
        target = int(input("Enter the value you want to search for:"))
        search(target)

    if inp == "print" or inp == "3":
        display()

    if inp == "delete" or inp == "4":
        target = int(input("Enter value to be deleted:"))
        delete(target)

def keypress_handler(key):
    if key == pg.K_q:
        Running = False
        pg.quit() 

    if key == pg.K_UP:
        if selected_node < node_count - 1:   
            selected_node += 1

    if key == pg.K_DOWN:
        if selected_node > 0:
            selected_node -= 1

    #insert random data
    if key == pg.K_r:
        insert(random.randint(0,100))

def click_handler(button):
    if button == 3:
        input_handler(input("Enter the command or type 'menu' to see commands:"))

def event_handler(event):
    if event.type == pg.QUIT:
            Running = False
            pg.quit()

    if event.type == pg.MOUSEBUTTONDOWN:
        click_handler(event.button)

    if event.type == pg.KEYDOWN:
        keypress_handler(event.key)

Running = True
clock = pg.time.Clock()
insert(20)
insert(30)

while Running:
    #clears the canvas
    canvas.fill((113,90,90))

    #itering over all nodes and calling their draw & update funcs
    
    rh = head
    while rh.next != None:
        rh.draw()
        rh.update()
        rh = rh.next
    rh.draw()
    rh.update()

    #after drawing on surface, bliting them to the main window (alpha stuff)
    #blits this canvas to window
    pg.Surface.blit(window,canvas,(0,0))

    clock.tick(60)#setting a constant framerate to ensure it runs at constant speed
    pg.display.flip()#brings the display on screen

    for event in pg.event.get():
        event_handler(event)
    
