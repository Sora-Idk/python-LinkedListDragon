import pygame as pg
import math
import random

pg.init()


window_size = [600,600]
window = pg.display.set_mode(window_size)
canvas = pg.Surface(window_size,pg.SRCALPHA)
font = pg.font.SysFont(None, 36) 
node_count = 1 # keeping the count of how long the body is, We atleast have head so hence 1
selected_node = 0#which node's info is being displayed?


#we will use linked list to store the dragon's body, and its attributes and its functions

#defining class Node
class Node:
    def __init__(self,index,data):
        self.prev = None
        self.next = None
        self.index = index
        self.data = data
        self.xpos = 0
        self.ypos = 0
        self.size = 0 # gets updated immidiately

    def __str__(self):
        return f"index:{self.index},data:{self.data},xpos:{self.xpos},ypos:{self.ypos}"
    
    def draw(self):
        if self.prev == None:
            pg.draw.circle(canvas,(0,0,255),(self.xpos,self.ypos),self.size)#draws the head
        else:
            pg.draw.circle(canvas,(255,0,0,80), (self.xpos,self.ypos), self.size)

        
        if self.index == selected_node:
            pg.draw.circle(canvas,(0,255,0),(self.xpos,self.ypos),self.size,3)

        text = font.render(str(self.data), True, (255,255,255))
        text_rect = text.get_rect(center=(self.xpos,self.ypos))

        # blit text onto *the same* canvas surface
        canvas.blit(text, text_rect)

    def update(self):
        #changing the size of the Node based on its position in the list-
        self.size = int(30 - (self.index * (30 - 20) / max(1, node_count)))

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
    canvas.fill((0,0,0))

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
    