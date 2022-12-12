import pygame
from pygame import display
import random
import math
from pygame.locals import *
from pygame.mouse import set_pos


pygame.init()
                                # width, height
screen = pygame.display.set_mode((1080,630))

background = pygame.image.load("field_newst.jpg")

pygame.display.set_caption("Air Hockey")
icon = pygame.image.load("air-hockey.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
pygame.display.flip()
clock.tick(30)


class striker(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        #self.speed = 0
        #self.angle = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (237, 66, 78), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (156, 0, 26), (self.x, self.y), self.radius - (self.radius / 2))

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > 1004 - self.radius:
            self.x = 2 * (1004 - self.radius) - self.x
            self.angle = - self.angle
        elif self.x < 112 - self.radius :
            self.x = 2 * (112-self.radius) - self.x
            self.angle = - self.angle
        if self.y > 578 - self.radius:
            self.y = 2 * (578 - self.radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y < 93 - self.radius:
            self.y = 2 * (93-self.radius) - self.y
            self.angle = math.pi - self.angle
            
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent
        angle1 = 2 * tangent - p1.angle
        speed1 = p1.speed
        (p1.angle, p1.speed) = (angle1, speed1)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)



class ball(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius-5)
    
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > 1004 - self.radius:
            self.x = 2 * (1004 - self.radius) - self.x
            self.angle = - self.angle
        elif self.x < 112 - self.radius :
            self.x = 2 * (112-self.radius) - self.x
            self.angle = - self.angle
        if self.y > 578 - self.radius:
            self.y = 2 * (578 - self.radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y < 93 - self.radius:
            self.y = 2 * (93-self.radius) - self.y
            self.angle = math.pi - self.angle
            
     
puck = ball(540, 308, 20, (59,61,64))

puck.speed = 2.1
puck.angle = random.choice([0,math.pi])

clicked = False

#Computer
compdraw = striker(120, 315, 36)
compdraw.speed = 2
compdraw.angle = math.atan2(compdraw.y-puck.y,puck.x-compdraw.x)
#math.atan((compdraw.x-puck.x)/(compdraw.y-puck.y))

p1_score = 0
opponent_score = 0

running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    mx = 980
    my = 285

    mx, my = pygame.mouse.get_pos()
    
    p1draw = striker(mx, my, 36)


    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render(f'{opponent_score} : {p1_score}', True, (215, 0, 64))


    if pygame.mouse.get_pos()[1] < 93:
        pygame.mouse.set_pos([mx,93])
    elif pygame.mouse.get_pos()[1] > 578 - p1draw.radius:
        pygame.mouse.set_pos([mx,578 - p1draw.radius])
    if pygame.mouse.get_pos()[0] < 112 :
        pygame.mouse.set_pos([112,my])
    elif pygame.mouse.get_pos()[0] > 1004 - p1draw.radius:
        pygame.mouse.set_pos([1004 - p1draw.radius,my])
    if pygame.mouse.get_pos()[0] < 540 + p1draw.radius:
        pygame.mouse.set_pos([540 + p1draw.radius,my])

    if compdraw.y < 93:
        compdraw.y = 93
    if compdraw.y > 578 - compdraw.radius:
        compdraw.y = 578 - compdraw.radius
    if compdraw.x < 112:
        compdraw.x = 112
    if compdraw.x > 540 - compdraw.radius:
        compdraw.x = 540 - p1draw.radius
    
    paused = False

    pygame.mouse.set_visible(False)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("You quit!")
                running = False
            if event.key == pygame.K_p:
                paused = True
            if event.key == pygame.K_u:
                paused = False
        
    
    puck_paddle_distance = math.sqrt((puck.x-mx)**2 + (puck.y-my)**2)
    if puck.x <= 93 and 270 <= puck.y <= 410 :
        p1_score += 1
        puck.x = 540
        puck.y = 308
        compdraw.x = 120
        compdraw.y = 315
        mx = 980
        my = 285
        print(p1_score)
        puck.angle = random.choice([0,math.pi])
    
    if puck.x >= 983 and 270 <= puck.y<= 410 :
        opponent_score += 1
        puck.x = 540
        puck.y = 308
        compdraw.x = 120
        compdraw.y = 315
        mx = 980
        my = 285
        print(p1_score)
        puck.angle = random.choice([0,math.pi])
    
    p1_ball = math.dist(list(pygame.mouse.get_pos()),[puck.x,puck.y])
    cp_ball = math.dist((compdraw.x,compdraw.y),[puck.x,puck.y])

    if cp_ball <= p1_ball and puck.x < 540:
        compdraw.speed = 2.25
        compdraw.angle = math.atan2(compdraw.y-puck.y,puck.x-compdraw.x)
    if puck.x < 540:
        compdraw.speed = 1
    elif puck.x >= 540:
        compdraw.speed = 1.5
        compdraw.angle = math.atan2(compdraw.y-random.randrange(300,390),random.randrange(99,150)-compdraw.x)

    # print(compdraw.x)
    # print(abs(puck.x-compdraw.x))
    # print(puck.x)

    if not paused:
        compdraw.move()
        puck.move()
        puck.bounce()
    collide(puck,compdraw)
    collide(puck,p1draw)
    puck.draw(screen)
    p1draw.draw(screen)
    compdraw.draw(screen)
    screen.blit(score,(520,4))
    pygame.display.update() # make all the changes at the end of each iteration

    #msg_font = pygame.font.Font("Helvetica.ttf",74)
    if p1_score == 3:
        print("Congratulations! You win.")
        end_text = font.render("Congratulations! You win.", True, (215, 0, 64))
        screen.blit(score,(540,280))
        pygame.display.flip()
        running = False
        
    elif opponent_score == 3:
        print("Too bad. Better luck next time.")
        end_text = font.render("Too bad. Better luck next time.", True, (215, 0, 64))
        screen.blit(score,(540,280))
        pygame.display.flip()
        running = False
        
    
    


"""
To do:
- 3 second timer
- Music
- Opponent
- Position P1 in goal
- Win/Lose message after 7 points
- EXTRAS
"""
