"""
Controlling a body indirectly, with a gravitational field.
The goal of the game is to get the indirectly controlled ball to the blue area.
"""
import pygame
import numpy as np
import time

###############################################################
#indirectly controlled body initial conditions:
x = 450
y = 400
vx = 0
vy = 0
dt = 0.01 #simulation accuracy
G = 6.61e-11
m = -1e+16 #if you make the masses negative, gravity just becomes antigravity :-)
#number of players - number of directly controlled gravitationally acting bodies
players = 2 #max 4!
p_speed = 5 #player speed (speed of indirectly controlled gravitationally acting bodies)
#you'll control these 4 bodies with: up-down-left-right arrows, wsda, tghf, iklj
###############################################################

pygame.init()

#define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)


#set up screen
SIZE = (600,500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Can you get control over (anti-)gravity?')

#sprites will be instances of this Body class:
class Body(pygame.sprite.Sprite):
    def __init__(self, colour, size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, colour, (size//2,size//2), size//2)
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
    def moveDown(self, pixels):
        self.rect.y += pixels
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    def moveRight(self, pixels):
        self.rect.x += pixels


#create sprites, initial conditions
#directly controlled bodies:
all_sprites = pygame.sprite.Group()
bodies = []
body1 = Body(ORANGE, 20)
body2 = Body(ORANGE, 20)
body3 = Body(ORANGE, 20)
body4 = Body(ORANGE, 20)
all_sprites.add(body1)
all_sprites.add(body2)
all_sprites.add(body3)
all_sprites.add(body4)
bodies.extend((body1, body2, body3, body4))


#main game loop:
carryOn = True
clock = pygame.time.Clock()

start_time = time.clock()
while carryOn:
    #EVENT HANDLING
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            carryOn = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_x:
                carryOn = False
            
    keys = pygame.key.get_pressed()
    #body1:
    if keys[pygame.K_LEFT]:
        body1.moveLeft(p_speed)
    if keys[pygame.K_RIGHT]:
        body1.moveRight(p_speed)
    if keys[pygame.K_UP]:
        body1.moveUp(p_speed)
    if keys[pygame.K_DOWN]:
        body1.moveDown(p_speed)
    #body2:
    if keys[pygame.K_w]:
        body2.moveUp(p_speed)
    if keys[pygame.K_s]:
        body2.moveDown(p_speed)
    if keys[pygame.K_a]:
        body2.moveLeft(p_speed)
    if keys[pygame.K_d]:
        body2.moveRight(p_speed)
    #body3:
    if keys[pygame.K_t]:
        body3.moveUp(p_speed)
    if keys[pygame.K_g]:
        body3.moveDown(p_speed)
    if keys[pygame.K_f]:
        body3.moveLeft(p_speed)
    if keys[pygame.K_h]:
        body3.moveRight(p_speed)
    #body4:
    if keys[pygame.K_i]:
        body4.moveUp(p_speed)
    if keys[pygame.K_k]:
        body4.moveDown(p_speed)
    if keys[pygame.K_j]:
        body4.moveLeft(p_speed)
    if keys[pygame.K_l]:
        body4.moveRight(p_speed)
        
    #GAME LOGIC
    #apply forces on the indirectly controlled body
    ax = 0
    ay = 0
    counter = 0
    for body in bodies:
        counter +=1
        if counter>players:
            break
        if body.rect.x > x:
            theta = np.arctan((body.rect.y-y)/(body.rect.x-x))
        elif body.rect.x < x:
            theta = np.arctan((body.rect.y-y)/(body.rect.x-x))+np.pi
        else:
            if body.rect.y > y:
                theta = np.pi/2.
            else:
                theta = -np.pi/2.
        dist = ((body.rect.y-y)**2. + (body.rect.x-x)**2.)**0.5
        amag = G*m/(dist**2)
        ax += amag*np.cos(theta)
        ay += amag*np.sin(theta)
    x += vx*dt + ax*dt*dt/2.
    y += vy*dt + ay*dt*dt/2.
    vx += ax*dt
    vy += ay*dt
    
    #check collisions:
    if x>80 and x<180 and y>480:
        end_time = time.clock()
        game_time = end_time = start_time
        print('Congratulations! You won!')
        print('Your time was: {:.2} seconds'.format(game_time))
        break
    if x<20 or x>580 or y<20 or y>480: #outer walls
        print('You hit a wall! Game over.')
        carryOn = False
    if x>285 and x<315 and not (y>120 and y<220): #middle walls
        print('You hit a wall! Game over.')
        carryOn = False
        
    all_sprites.update()
    
    
    #GRAPHICS
    screen.fill(BLACK)
    pygame.draw.circle(screen, YELLOW, (int(x),int(y)), 10)
    all_sprites.draw(screen)
    #draw walls - collisions are checked above, these two pieces have to be adjusted together
    pygame.draw.rect(screen, RED, [0,0, 600,10]) #top wall
    pygame.draw.rect(screen, RED, [0,0, 10,500]) #left wall
    pygame.draw.rect(screen, RED, [590,0, 10,500]) #right wall
    pygame.draw.rect(screen, RED, [0,490, 600,10]) #bottom wall
    pygame.draw.rect(screen, RED, [295,230, 10,260]) #obstacle 1
    pygame.draw.rect(screen, RED, [295,10, 10,100]) #obstacle 2
    pygame.draw.rect(screen, BLUE, [80,490, 100,10]) #finish line
    
    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()