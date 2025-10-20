import pygame as pg
import math

pg.init()

window = pg.display.set_mode((512,512))

x,y = 200,200
size = 30
points = [(x-10,y+7),(x-10,y-2),(x-6,y-9),(x-2,y-15),(x+2,y-15),(x+6,y-9),(x+10,y-2),(x+10,y+7),(x+9,y+8),(x+7,y+6),(x+4,y+6),(x+4,y+9),(x,y+15),(x-4,y+9),(x-4,y+6),(x-2,y+5),(x-6,y+5),(x-10,y+7)]

points_head = [(x+0*size//10,y+15*size//10),(x+2*size//10,y+11*size//10),(x+3*size//10,y+8*size//10),(x+3*size//10,y+4*size//10),(x+6*size//10,y+4*size//10),(x+10*size//10,y+7*size//10),(x+10*size//10,y+-3*size//10),(x+6*size//10,y+-11*size//10),(x+2*size//10,y+-15*size//10),(x+-2*size//10,y+-15*size//10),(x+-6*size//10,y+-11*size//10),(x+-10*size//10,y+-3*size//10),(x+-10*size//10,y+7*size//10),(x+-6*size//10,y+4*size//10),(x+-3*size//10,y+4*size//10),(x+-3*size//10,y+8*size//10),(x+-2*size//10,y+11*size//10),]
points_right_eye = [(x+2*size//10,y+-8*size//10),(x+4*size//10,y+-7*size//10),(x+5*size//10,y+-5*size//10),(x+5*size//10,y+-3*size//10),(x+2*size//10,y+-5*size//10),]
points_left_eye = [(x+-2*size//10,y+-8*size//10),(x+-4*size//10,y+-7*size//10),(x+-5*size//10,y+-5*size//10),(x+-5*size//10,y+-3*size//10),(x+-2*size//10,y+-5*size//10)]

x,y=400,400
points_body = [(x+0*size//10,y+-14*size//10),(x+4*size//10,y+-12*size//10),(x+7*size//10,y+-9*size//10),(x+5*size//10,y+-7*size//10),(x+5*size//10,y+-5*size//10),(x+8*size//10,y+-2*size//10),(x+10*size//10,y+2*size//10),(x+10*size//10,y+6*size//10),(x+6*size//10,y+1*size//10),(x+4*size//10,y+1*size//10),(x+2*size//10,y+7*size//10),(x+0*size//10,y+14*size//10),(x+-2*size//10,y+7*size//10),(x+-4*size//10,y+1*size//10),(x+-6*size//10,y+1*size//10),(x+-10*size//10,y+6*size//10),(x+-10*size//10,y+2*size//10),(x+-8*size//10,y+-2*size//10),(x+-5*size//10,y+-5*size//10),(x+-5*size//10,y+-7*size//10),(x+-7*size//10,y+-9*size//10),(x+-4*size//10,y+-12*size//10)]

p_head = [[0, 15], [2, 11], [3, 8], [3, 4], [6, 4], [10, 7], [10, -3], [6, -11], [2, -15], [-2, -15], [-6, -11], [-10, -3], [-10, 7], [-6, 4], [-3, 4], [-3, 8], [-2, 11]]
p_leye = [[-2, -8], [-4, -7], [-5, -5], [-5, -3], [-2, -5]]
p_reye = [[2, -8], [4, -7], [5, -5], [5, -3], [2, -5]]
p_body = [[0,-14],[4,-12],[7,-9],[5,-7],[5,-5],[8,-2],[10,2],[10,6],[6,1],[4,1],[2,7],[0,14],[-2,7],[-4,1],[-6,1],[-10,6],[-10,2],[-8,-2],[-5,-5],[-5,-7],[-7,-9],[-4,-12]]

def rotate_point(px, py, angle_deg):
    rad = math.radians(angle_deg)
    x_new = px * math.cos(rad) - py * math.sin(rad)
    y_new = px * math.sin(rad) + py * math.cos(rad)
    return [x_new, y_new]

running = True
while running:
    #put this code inside ever node, in update.
    pg.Surface.fill(window,(0,0,0))
    size = 2


    px,py = 200,200
    mx,my = pg.mouse.get_pos()
    dx, dy = mx - px, my - py
    angle = math.degrees(math.atan2(-dy, dx)) -90

    #rotated = [rotate_point(x*size, y*size, -angle) for x,y in p_body]

    #p_b = [[px+x*size, py+y*size] for x,y in p_body]# change size with self.size, px with self.prev.xpos and py with self.prev.ypos
    p_h = [[px + x, py + y] for x,y in [rotate_point(x*size, y*size, -angle) for x,y in p_head]]
    p_le = [[px + x, py + y] for x,y in [rotate_point(x*size, y*size, -angle) for x,y in p_leye]]
    p_re = [[px + x, py + y] for x,y in [rotate_point(x*size, y*size, -angle) for x,y in p_reye]]

    px,py = 400,400
    mx,my = pg.mouse.get_pos()
    dx, dy = mx - px, my - py
    angle = math.degrees(math.atan2(-dy, dx)) -90
    p_b = [[px + x, py + y] for x,y in [rotate_point(x*size, y*size, -angle) for x,y in p_body]]


    #head 
    pg.draw.polygon(window,(255,255,255),p_h,3)
    pg.draw.polygon(window,(255,255,255),p_le,3)
    pg.draw.polygon(window,(255,255,255),p_re,3)

    #body
    pg.draw.polygon(window,(255,255,255),p_b,3)


    
    pg.draw.circle(window,(0,255,0),(x,y),2)

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                running = False