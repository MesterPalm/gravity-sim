import pygame
import sys
from time import sleep, perf_counter
import os
from math import sin, cos

##SETTING VARS
#display settings
SCALE = 2.5
SCREEN_WIDTH = 640*SCALE
SCREEN_HEIGHT = 480*SCALE
PLANET_SCALE = 1

#colors
white = (255,255,255)
red = (255,50,50)
green = (50,255,50)
blue = (50,50,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
space_grey = (15,10,15)
planet_red = (185,50,80)
planet_green = (150, 200, 75)
planet_blue = (20, 150, 170)



#simulation settings
GRAVITONS=0.2
TIME_SCALE = 10

##SETTUP
pygame.init()
screen = pygame.display.set_mode((int(SCREEN_WIDTH),int(SCREEN_HEIGHT)), pygame.RESIZABLE)
playin = True
log = {}
pause = False
step = False
draw_offset = [0,0]
draw_scale = 1
button_held = False

planets = []
clear = lambda: os.system('clear')
curr_time = 0
mouse_pos= pygame.mouse.get_pos()
scroll_scale_change = 0.1
    
class planet:
    def __init__(self, pos, color, mass):
        self.pos = pos
        self.color = color
        self.mass = mass
        self.velocity = [0,0]
        self.force = [0,0]

    def add_force(self, push_force):
        self.force[0] += push_force[0]
        self.force[1] += push_force[1]

    def gravity_between(self, other):
        global GRAVITONS, log
        direction = [other.pos[0] - self.pos[0], other.pos[1] - self.pos[1]]
        distance_sqrd = (self.pos[0] - other.pos[0])**2 + (self.pos[1] - other.pos[1])**2
        direction[0] = direction[0]/(distance_sqrd**(1/2))
        direction[1] = direction[1]/(distance_sqrd**(1/2))
        f = GRAVITONS*self.mass*other.mass/distance_sqrd
        return (direction[0]*f, direction[1]*f)

    def update(self, delta_time=1):
        delta_time = 1 if delta_time > 1 else delta_time
        time_step = delta_time*TIME_SCALE
        self.velocity[0] += time_step*self.force[0]/self.mass
        self.velocity[1] += time_step*self.force[1]/self.mass
        self.force = [0,0]
        self.pos[0] += self.velocity[0]*time_step
        self.pos[1] += self.velocity[1]*time_step

planets.append(planet([0,0], planet_blue, 100000))
planets.append(planet([5*SCREEN_WIDTH, 5*SCREEN_HEIGHT], planet_blue, 100000))
planets.append(planet([2*SCREEN_WIDTH, 2*SCREEN_HEIGHT], planet_green, 1500000))
planets[0].add_force([-40000,40000])
planets[1].add_force([50000,-50000])
nr =70
start = 100
radius = 1/200
angle = 1
for i in range(start,start+nr):
    planets.append(planet([i*SCREEN_WIDTH*cos(i*angle)*radius+SCREEN_HEIGHT/3, i*SCREEN_HEIGHT*sin(i*angle)*radius+SCREEN_HEIGHT/3], [i*255/(nr+start),255,255/(i+1)], 5*(1 + (i%3))))
for i in range(start,start+nr):
    planets.append(planet([i*SCREEN_WIDTH*cos(i*angle)*radius+6*SCREEN_HEIGHT, i*SCREEN_HEIGHT*sin(i*angle)*radius+6*SCREEN_HEIGHT], [i*255/(nr+start),255,255/(i+1)], 5*(1 + (i%3))))

##MAIN LOOP
while (playin):  
    prev_time = curr_time
    curr_time = perf_counter()
    delta_time = curr_time - prev_time
    log["dtime"] = "delta time: " + str(delta_time)
    #game logic
    if not pause or step:
        step = False
        for p1 in planets:
            for p2 in planets:
                if p1 != p2:
                    p1.add_force(p1.gravity_between(p2))
                    #add normal force
    
        for planet in planets:
            planet.update(delta_time)
    #drawing
    screen.fill(space_grey)
    for planet in planets:
        pygame.draw.circle(screen, planet.color, (int(draw_scale*(planet.pos[0]) + draw_offset[0]), int(draw_scale*(planet.pos[1]) + draw_offset[1])), int(draw_scale*PLANET_SCALE*(planet.mass)**(1/3)))
   
    #event handling
    prev_mouse_pos = mouse_pos
    mouse_pos= pygame.mouse.get_pos()

    for event in pygame.event.get():
        log["event"] = str(event)
        if event.type == pygame.QUIT:
            playin = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_s:
                step = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_held = True
            if event.button == 4:
                draw_scale = draw_scale*(1-scroll_scale_change)
                draw_offset[0] += mouse_pos[0]*scroll_scale_change
                draw_offset[1] += mouse_pos[1]*scroll_scale_change
            elif event.button == 5:     
                draw_scale = draw_scale*(1+scroll_scale_change)
                draw_offset[0] -= mouse_pos[0]*scroll_scale_change
                draw_offset[1] -= mouse_pos[1]*scroll_scale_change

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_held = False
                
    if button_held == True:
        mouse_motion = [mouse_pos[0]-prev_mouse_pos[0],mouse_pos[1]-prev_mouse_pos[1]]
        draw_offset[0] += mouse_motion[0]
        draw_offset[1] += mouse_motion[1]
    clear()
    for key in log:
        print(log[key])
    pygame.display.update()

#quitting
pygame.quit()
exit()
