import pygame
import sys
from time import sleep, perf_counter
import os

##SETTING VARS
#display settings
SCALE = 3
SCREEN_WIDTH = 640*SCALE
SCREEN_HEIGHT = 480*SCALE
PLANET_SCALE = 2

#colors
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

#simulation settings
GRAVITONS=0.5
TIME_SCALE = 10

##SETTUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE)
playin = True
log = {}
pause = False
step = False

planets = []
clear = lambda: os.system('clear')
curr_time = 0


    
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
        print(delta_time)
        delta_time = 1 if delta_time > 1 else delta_time
        time_step = delta_time*TIME_SCALE
        self.velocity[0] += time_step*self.force[0]/self.mass
        self.velocity[1] += time_step*self.force[1]/self.mass
        self.force = [0,0]
        self.pos[0] += self.velocity[0]*time_step
        self.pos[1] += self.velocity[1]*time_step

planets.append(planet([SCREEN_WIDTH/4, SCREEN_HEIGHT/4], green, 20))
planets.append(planet([3*SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4], red, 20))
planets.append(planet([SCREEN_WIDTH/4, 3*SCREEN_HEIGHT/4], pink, 20))
planets.append(planet([3*SCREEN_WIDTH/4, SCREEN_HEIGHT/4], blue, 20))
planets.append(planet([SCREEN_WIDTH/5, SCREEN_HEIGHT/5], green, 10))
planets.append(planet([4*SCREEN_WIDTH/5, 4*SCREEN_HEIGHT/5], red, 10))
planets.append(planet([4*SCREEN_WIDTH/5, SCREEN_HEIGHT/5], green, 10))
planets.append(planet([SCREEN_WIDTH/5, 4*SCREEN_HEIGHT/5], red, 10))
planets.append(planet([SCREEN_WIDTH/2, SCREEN_HEIGHT/2], blue, 10000))
planets[0].add_force([4,-4])
planets[1].add_force([-4,4])
planets[2].add_force([2,-4])
planets[3].add_force([0,4])
planets[4].add_force([4,0])
planets[5].add_force([-4,0])
planets[6].add_force([0,4])
planets[7].add_force([0,-4])
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
    
        for planet in planets:
            planet.update(delta_time)
    #drawing
    screen.fill(darkBlue)
    for planet in planets:
        print(screen, planet.color, (int(planet.pos[0]), int(planet.pos[1])), int(PLANET_SCALE*(planet.mass)**(1/3)))
        pygame.draw.circle(screen, planet.color, (int(planet.pos[0]), int(planet.pos[1])), int(PLANET_SCALE*(planet.mass)**(1/3)))

    #sleep(0.01)
   
    #event handling
    for event in pygame.event.get():
        log["event"] = str(event)
        if event.type == pygame.QUIT:
            playin = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_s:
                step = True
            
    clear()
    for key in log:
        print(log[key])
    pygame.display.update()

#quitting
pygame.quit()
exit()
