import pygame
import ast
import math
def fontBox(d,font,text,(posx,posy),color=(255,255,255)):
    t = font.render(text,255,color)
    r = t.get_rect(center=(posx,posy))
    d.blit(t,r)
    return r
def sliderBox(d,pos,(length,width),bar_value):
    bbar = pygame.draw.rect(d,(150,150,150),(pos[0],pos[1],100*length,width))
    baar = pygame.draw.rect(d,(255,255,255),(pos[0],pos[1],bar_value*100*length,width))
    mouserect = pygame.rect.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],2,2)
    font2 = pygame.font.SysFont(None,20)
    fontBox(d,font2,str(bar_value),(pos[0]+45*length,pos[1]+7.5),(0,0,0))
    if mouserect.colliderect(bbar):
        if pygame.mouse.get_pressed()[0]:
            new_value = float(pygame.mouse.get_pos()[0]-pos[0])/100
            if new_value >= 0.98:
                new_value = 1.0
            return new_value
        else:
            return bar_value
    else:
        return bar_value
def img(path,addpath=''):
    if type(path) == list:
        listy = True
    else:
        listy = False
    try:
        if listy:
            listboi = []
            for i in path:
                listboi.append(pygame.image.load(addpath+i))
            return listboi
        else:
            return pygame.image.load(path)
    except IOError, e:
        print e
        surface_didnt_load = pygame.surface.Surface((50,50))
        surface_didnt_load.fill((255,0,0))
        return surface_didnt_load
def rotatePoint(origin,point,angle,debug=None):
    """Return-> (x,y). Where CX and CY reperesent the pivot point."""
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    if debug != None:
        pygame.draw.rect(debug,(0,255,0),(ox,oy,2,2))
        pygame.draw.rect(debug,(0,255,255),(qx,qy,2,2))


    return (qx, qy)
def loadsave():
    fileio = file('save')
    real_data = []
    other_data= fileio.readlines()
    for i in other_data:
        if i.startswith('DO NOT'):
            pass
        else:
            toread = i.replace('__B_N__','\n').decode('zip')
            real_data.append(ast.literal_eval(toread))
    return real_data
def savesave(data):
    fileio = file('save','w')
    real_data = []
    real_data.append("DO NOT MODIFY THIS FILE.\n")
    for i in data:
        if type(i) == str:
            i = "'" + i + "'"
        towrite = str(i).encode('zip').replace("\n","__B_N__") +'\n'
        real_data.append(towrite)
    fileio.writelines(real_data)
    fileio.close()
