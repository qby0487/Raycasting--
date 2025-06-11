import pygame
import math
import numpy as np

#screen
width = 640
height = 480
halfWidth = width/2
halfHeight = height/2    

scale = 4

#textureimage = pygame.image.load("texture.png")

#texture
textures = [
    {
    "width" : 8,
    "height" : 8,

    "bitmap" : [
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,0,0,0,1],
        [1,1,1,1,1,1,1,1],
        [0,1,0,0,0,1,0,0],
        [1,1,1,1,1,1,1,1],
        [0,0,0,1,0,0,0,1],
        [1,1,1,1,1,1,1,1],
        [0,1,0,0,0,1,0,0]
        ],
    "colors":[ (255, 241, 232),
                (194, 195, 199) ]
},
 {
            "width": 16,
            "height": 16,
            "id": "bricks.png",
            "data": None
        },
    {
            "width": 16,
            "height": 16,
            "id": "bricks.png",
            "data": None
    }


]
#projection

Pwidth = width / scale
Pheight = height / scale

halfPwidth = Pwidth/2
halfPheight = Pheight/2

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
radius = 10
'''
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,0,1,0,0,1],
        [1,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,1,0,0,1],
        [1,0,0,1,0,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1],'''
#    rayCasting
#incrementAngle = fov/width
incrementAngle = fov/Pwidth
precision = 64    
map =[
    [2,2,2,2,2,3,3,3,3,2],
    [2,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,3,0,0,0,0,2],
    [2,0,0,2,2,0,2,0,0,2],
    [2,0,0,2,0,0,2,0,0,2],
    [2,0,0,2,0,0,2,0,0,2],
    [2,0,0,2,0,2,2,0,0,2],
    [2,0,0,3,0,3,3,0,0,2],
    [2,0,0,0,0,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,2],
    ]

#def drawmap():


def loadtexture():
    for i in range(len(textures)):
        if "id" in textures[i]:
            if (textures[i]["id"]):
                textures[i]["data"] = gettexturedata(textures[i])

def gettexturedata(texture):
    image = pygame.image.load(texture["id"])
    canvas = pygame.Surface((texture["width"],texture["height"]))
    image = pygame.transform.scale(image,(texture["width"],texture["height"]))
   # canvas.blit(image,(0,0))

    imagedata = pygame.surfarray.array3d(image) #為何應該使用pixels3d而非arrays3d? 請搞懂 #解答:兩者都可以使用且array3d可能更加安全
    return parseimagedata(imagedata)
def parseimagedata(imagedata):
    colorarray = []
    #for i in range(len(imagedata)):
    #    colorarray.append((imagedata[i],imagedata[i+1],imagedata[i+2]))
#以下for迴圈是AI寫的，將由之後搞懂原因 解答:將2D的陣列轉為1D的 imagedata.shape[1] 代表圖像的高度（Y軸像素數）imagedata.shape[0] 代表圖像的寬度（X軸像素數）
    for y in range(imagedata.shape[1]):
        row_colors = []
        for x in range(imagedata.shape[0]):
            # Extract RGB values
            r, g, b = imagedata[x, y]
            row_colors.append((r, g, b))
        colorarray.extend(row_colors)
#到這邊都是
    return colorarray

def drawtexture(screen,x,wallHeight,textureX,texture):
    Yincrementer = (wallHeight * 2) /texture["height"]
    y = halfPheight - wallHeight

    for i in range(texture["height"]):
        if texture["id"]:
            texturecolor = texture["data"][textureX + i * texture["width"]]
        else:    
            colorindex = texture["bitmap"][i][textureX]
            texturecolor = texture["colors"][colorindex]
        
        
        pygame.draw.line(screen,texturecolor,(x,y),(x,y + (Yincrementer + 0.5)))
        y += Yincrementer


def raycast(screen):
    rayangle = angle - halfFov
  #  for (rayCount = 0, rayCount < width, rayCount++):
    for rayCount in range(int(Pwidth)):
        
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


        wallheight = int(halfPheight/distance)

        texture = textures[wall-1]

        textureX = int((texture["width"] * (ray_x + ray_y)) % texture["width"])

        pygame.draw.line(screen,"black",(rayCount,0),(rayCount,halfPheight - wallheight))
    #    pygame.draw.line(screen,(200,200,200),(rayCount,halfPheight - wallheight),(rayCount,halfPheight + wallheight))
        drawtexture(screen,rayCount,wallheight,textureX,texture)
        pygame.draw.line(screen,(95,87,79),(rayCount,halfPheight + wallheight),(rayCount,Pheight))
        rayangle += incrementAngle
'''
        pygame.draw.line(screen,(0,128,128),(rayCount,0),(rayCount,halfPheight - wallheight))
        pygame.draw.line(screen,(200,200,200),(rayCount,halfPheight - wallheight),(rayCount,halfPheight + wallheight))
        pygame.draw.line(screen,(0,100,0),(rayCount,halfPheight + wallheight),(rayCount,Pheight))
'''


def movements():

    global x ,y ,angle
    keys = pygame.key.get_pressed()


    if keys[pygame.K_w]:
        playercos = math.cos(math.radians(angle))*speed
        playersin = math.sin(math.radians(angle))*speed
        newx = x + playercos
        newy = y + playersin
        checkx = int(newx + playercos * radius)
        checky = int(newy + playercos * radius)

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
    surface = pygame.Surface((Pwidth, Pheight))
    screen = pygame.display.set_mode((width , height ))
    
    pygame.display.set_caption("3D MAZE")
    
    clock = pygame.time.Clock()

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #movement 

        movements()
       
        surface.fill((0,0,0))
        raycast(surface)
        #drawmap(surface)
        scaled_surface = pygame.transform.scale(surface, (width, height ))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
    
        clock.tick(1000 / delay)
   
    pygame.quit() 

loadtexture()
main()