import pygame as pg

pg.init()
window = pg.display.set_mode((512,512))
canvas = pg.Surface((512,512),pg.SRCALPHA)

#delaring the head as none
head = None
node_count = 0 # keeping the count of how long the body is

#we will use linked list to store the dragon's body, and its attributes and its functions

#defining class Node
class Node:
    def __init__(self,index,next= None,prev = None):
        self.prev = prev
        self.next = next
        self.index = index
        self.xpos = None
        self.ypos = None
        self.size = 50
    def __str__(self):
        return f"index:{self.index},xpos:{self.xpos},ypos:{self.ypos}"

def insert(index,spawning = False):
    global head, node_count
    if head == None:
        head = Node(index = index)
        head.xpos,head.ypos = 0,0
    else:
        rh = head
        while rh.next != None:
            rh = rh.next
        rh.next = Node(index = index)
        rh.next.prev = rh
        if spawning:
            rh.next.xpos,rh.next.ypos = 0,0
        else:
            rh.next.xpos,rh.next.ypos = rh.xpos-(-1*(rh.prev.xpos-rh.xpos)),rh.ypos-(-1*(rh.prev.ypos-rh.ypos))
        
    node_count += 1

def draw():
    global head
    rh = head

    #clears the canvas
    canvas.fill((0,0,0))
    

    while rh.next!= None:
        pg.draw.circle(canvas,(255,0,0,80), (rh.xpos,rh.ypos), rh.size)
        rh = rh.next

    #draws the head
    pg.draw.circle(canvas,(0,0,255),(head.xpos,head.ypos),head.size)

    #blits this canvas to window
    pg.Surface.blit(window,canvas,(0,0))

def update(Node:Node):
    #has the logic to update position based on cursor
    mouse_x, mouse_y = pg.mouse.get_pos()
    
    #changing the size of the Node based on its position in the list-
    Node.size = int(20 - (Node.index * (20 - 5) / max(1, node_count)))

    # Smoothing factor (0 < alpha < 1, smaller = slower follow)
    alpha = 0.1  

    #checking if node = head, if true it will follow cursor
    if Node.prev == None:
        # Smoothly move point towards mouse
        Node.xpos += (mouse_x - Node.xpos) * alpha
        Node.ypos += (mouse_y - Node.ypos) * alpha
    #if not head, It will follow its previous node
    else:
        Node.xpos += (Node.prev.xpos - Node.xpos) * alpha
        Node.ypos += (Node.prev.ypos - Node.ypos) * alpha

Running = True
clock = pg.time.Clock()

for i in range(5):
    insert(node_count,True)
while Running:
    if node_count >0:
        rh = head
        draw()
        while rh.prev == None or rh.next != None:
            update(rh)
            rh = rh.next

    clock.tick(60)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Running = False
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                insert(node_count)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                Running = False
                pg.quit() 
