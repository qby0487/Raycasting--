import pygame
import math
#import numpy as np

width = 640
height = 480
halfWidth = width/2
halfHeight = height/2    

#    render: 
delay = 30    

#    player:
fov = 60
halfFov = fov/2
x = 2
y = 2
angle = 90

#movement
speed = 0.1
rotation = 3.0

#    rayCasting
incrementAngle = fov/width
precision = 64    
map =[
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,0,1,0,0,1],
        [1,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,1,0,0,1],
        [1,0,0,1,0,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1],
    ]


'''
canva = pygame.Surface(screen.get_size())
canva = canva.convert()
screen.blit(canva, (0,0))
#screen.fill(0,0,0)
'''
#def drawmap():


def raycast(screen):
    rayangle = angle - halfFov
  #  for (rayCount = 0, rayCount < width, rayCount++):
    for rayCount in range(width):
        
        ray_x = x
        ray_y = y
        raycos= math.cos(math.radians(rayangle)) / precision
        raysin= math.sin(math.radians(rayangle)) / precision

        wall = 0
        while(wall == 0):
            ray_x += raycos
            ray_y += raysin
            wall = map[int(ray_y)][int(ray_x)]
    
        distance = math.sqrt(math.pow(x-ray_x,2) + math.pow(y-ray_y,2))
        #fisheye fix(三角函數)
        distance = distance * math.cos(math.radians(rayangle - angle))


        wallheight = int(halfHeight/distance)

        pygame.draw.line(screen,(0,128,128),(rayCount,0),(rayCount,halfHeight - wallheight))
        pygame.draw.line(screen,(200,200,200),(rayCount,halfHeight - wallheight),(rayCount,halfHeight + wallheight))
        pygame.draw.line(screen,(0,100,0),(rayCount,halfHeight + wallheight),(rayCount,height))
        rayangle += incrementAngle
def movements():

    global x ,y ,angle
    keys = pygame.key.get_pressed()


    if keys[pygame.K_w]:
        playercos = math.cos(math.radians(angle))*speed
        playersin = math.sin(math.radians(angle))*speed
        newx = x + playercos
        newy = y + playersin
        if map[int(newy)][int(newx)] == 0:
            x = newx
            y = newy
    elif keys[pygame.K_s]:
        playercos = math.cos(math.radians(angle))*speed
        playersin = math.sin(math.radians(angle))*speed
        newx = x - playercos
        newy = y - playersin
        if map[int(newy)][int(newx)] == 0:
            x = newx
            y = newy
    if keys[pygame.K_d]:
        angle += rotation
        if angle > 360:
            angle -= 360
    elif keys[pygame.K_a]:
        angle -= rotation
        if angle < 0:
            angle += 360



def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("3D MAZE")
    clock = pygame.time.Clock()

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #movement 

        movements()
       
        screen.fill((0,0,0))
        raycast(screen)
    
        pygame.display.flip()
    
        clock.tick(1000 / delay)
   
    pygame.quit() 

main()





'''
等於math.radians()
def DegreetoRaidans(degree):
    pi = math.pi
    return degree * pi /180
'''

'''
pygame.draw.line(畫布, 顏色, (x坐標1, y坐標1), (x坐標2, y坐標2), 線寬)4
                (x1, y1, x2, y2, cssColor
drawLine(rayCount, 0, rayCount, data.screen.halfHeight - wallHeight, "cyan");
drawLine(rayCount, data.screen.halfHeight - wallHeight, rayCount, data.screen.halfHeight + wallHeight, "red");
drawLine(rayCount, data.screen.halfHeight + wallHeight, rayCount, data.screen.height, "green");
'''
