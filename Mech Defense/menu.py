import pygame
import images
import main
import os
from funct import *
import funct
pygame.font.init()
pygame.mixer.init()

class menu():
    def __init__(self,a):
        pygame.mixer.stop()
        music = pygame.mixer.Sound("data/music/menu.ogg")
        version = "v0.0.0"
        running = 1
        display = pygame.display.set_mode((800,600))
        music = music.play()
        clock = pygame.time.Clock()
        anim_times = [278,187,265,0,0]
        anim_time_c = anim_times[0]
        if a == 0:
            animframe = 3
        else:
            animframe = 3
        splash_image = 0
        font = pygame.font.SysFont(None,40)
        font2= pygame.font.SysFont(None,20)


        playpos = 200
        wanttoplay = 0
        bar_value = funct.savedata[0]
        bar_value2 = funct.savedata[1]
        music.set_volume(bar_value)
        screen = 0
        sub_screen = 0
        sub__screen = 0
        editing = [False,False,False,False,False]
        click_cooldown = 3
        editing_cooldown = 5
        running = True
        while running:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                        music.stop()
                        
            if animframe <= 2:
                anim_time_c -= 1
            if anim_time_c <= 0:
                animframe += 1
                anim_time_c = anim_times[animframe]
                if animframe >= 3:
                    animframe = 3
            display.blit(images.splash[animframe],(0,0))
            fontBox(display,font2,version,(770,585))
            mousepos = pygame.mouse.get_pos()
            mouse = pygame.rect.Rect(mousepos[0],mousepos[1],2,2)
            click_cooldown -= 1
            if click_cooldown < 0:
                click = pygame.mouse.get_pressed()[0]
                click_cooldown = 5
            else:
                click = 0
            if animframe == 3:
                if screen == 0:
                    playButton = fontBox(display,font,"play",(600,playpos))
                    settingsButton = fontBox(display,font,"settings",(600,230))
                    inventoryButton = fontBox(display,font,"inventory",(600,260))
                    exitButton = fontBox(display,font,"exit",(600,290))
                    if exitButton.colliderect(mouse):
                        if click:
                            music.stop()
                            savesave(savedata)
                            running = False
                    if settingsButton.colliderect(mouse):
                        if click:
                            screen = 1
                            sub_screen = 0
                    if inventoryButton.colliderect(mouse):
                        if click:
                            screen = 2
                            sub__screen = 0
                    if playButton.colliderect(mouse):
                        wanttoplay = 60
                    wanttoplay -= 1
                    if wanttoplay >= 0:
                        if playpos >= 170:
                            playpos -= 1
                        if playpos <= 171:
                            host = fontBox(display,font,"host",(570,200))
                            join = fontBox(display,font,"join",(630,200))
                            if host.colliderect(mouse):
                                wanttoplay = 60
                                if click:
                                    music.stop()
                                    main.main(True)
                            if join.colliderect(mouse):
                                wanttoplay = 60
                                if click:
                                    main.main(False)

                    elif wanttoplay <= 0:
                        if playpos <= 198:
                            playpos += 1
                elif screen == 1:
                    """Settings"""
                    if sub_screen == 0:
                        """Settings home"""
                        sdisplay = fontBox(display,font,"display",(600,200))
                        sounds = fontBox(display,font,"sound",(600,230))
                        multiplayers = fontBox(display,font,"multiplayer",(600,260))
                        exitButton = fontBox(display,font,"back",(600,290))
                        if sdisplay.colliderect(mouse):
                            if click:
                                sub_screen = 1
                        if sounds.colliderect(mouse):
                            if click:
                                sub_screen = 2
                        if multiplayers.colliderect(mouse):
                            if click:
                                sub_screen = 3
                        if exitButton.colliderect(mouse):
                            if click:
                                savesave(funct.savedata)
                                screen = 0
                                sub_screen = 0
                    elif sub_screen == 1:
                        """Display"""
                        if funct.savedata[2]:
                            fullscreen = fontBox(display,font,"fullscreen - Y",(600,260))
                        else:
                            fullscreen = fontBox(display,font,"fullscreen - N",(600,260))
                        exitButton = fontBox(display,font,"back",(600,290))
                        if fullscreen.colliderect(mouse):
                            if click:
                                funct.savedata[2] = not funct.savedata[2]
                        if exitButton.colliderect(mouse):
                            if click:
                                savesave(funct.savedata)
                                if funct.savedata[2]:
                                    display = pygame.display.set_mode((800,600),pygame.FULLSCREEN)
                                else:
                                    display = pygame.display.set_mode((800,600))
                                sub_screen = 0
                    elif sub_screen == 2:
                        """Sound"""
                        msc = fontBox(display,font,"music volume",(600,260))
                        sfx = fontBox(display,font,"sfx volume",(600,320))
                        exitButton = fontBox(display,font,"back",(600,380))
                        bar_value = sliderBox(display,(550,280),(1,20),bar_value)
                        bar_value2 = sliderBox(display,(550,340),(1,20),bar_value2)
                        music.set_volume(bar_value)
                        if exitButton.colliderect(mouse):
                            if click:
                                funct.savedata[0] = bar_value
                                funct.savedata[1] = bar_value2
                                sub_screen = 0
                    elif sub_screen == 3:
                        """Multiplayer"""
                        fontBox(display,font,"Host:",(600,170))
                        hip = fontBox(display,font,"IP:"+str(funct.savedata[3]),(600,200))
                        hport = fontBox(display,font,"Port:"+str(funct.savedata[4]),(600,230))
                        fontBox(display,font,"Client:",(600,260))
                        cip = fontBox(display,font,"IP: "+str(funct.savedata[5]),(600,290))
                        cport = fontBox(display,font,"Port: "+str(funct.savedata[6]),(600,320))
                        playername = fontBox(display,font,"Name: " + funct.savedata[7],(600,350))
                        exitButton = fontBox(display,font,"exit",(600,380))
                        if hip.colliderect(mouse):
                            if click:
                                editing[0] = True
                        elif hport.colliderect(mouse):
                            if click:
                                editing[1] = True
                        elif cip.colliderect(mouse):
                            if click:
                                editing[2] = True
                        elif cport.colliderect(mouse):
                            if click:
                                editing[3] = True
                        elif playername.colliderect(mouse):
                            if click:
                                editing[4] = True
                        if exitButton.colliderect(mouse):
                            if click:
                                sub_screen = 0
                                savesave(funct.savedata)
                        if True in editing:
                            key = pygame.key.get_pressed()
                            editing_cooldown -= 1
                            try:
                                if editing_cooldown <= 0:
                                    typed = chr(key.index(1))
                                    if key[pygame.K_LSHIFT]:
                                        typed = typed.upper()
                                    if key[pygame.K_BACKSPACE]:
                                        typed = 'back'
                                    elif key[pygame.K_RETURN]:
                                        typed = 'enter'
                                    editing_cooldown = 7
                                else:
                                    typed = ''
                            except:
                                typed = ''
                            if editing[0]:
                                if typed == 'back':
                                    funct.savedata[3] = funct.savedata[3][:-1]
                                elif typed == 'enter':
                                    editing[0] = False
                                else:
                                    funct.savedata[3] += typed
                            elif editing[1]:
                                if typed == 'back':
                                    funct.savedata[4] = int(str(funct.savedata[4])[:-1])
                                elif typed == 'enter':
                                    editing[1] = False
                                else:
                                    try: funct.savedata[4]  = int(str(funct.savedata[4]) + typed)
                                    except: pass
                            elif editing[2]:
                                if typed == 'back':
                                    funct.savedata[5] = funct.savedata[5][:-1]
                                elif typed == 'enter':
                                    editing[2] = False
                                else:
                                    funct.savedata[5] += typed
                            elif editing[3]:
                                if typed == 'back':
                                    funct.savedata[6] = int(str(funct.savedata[6])[:-1])
                                elif typed == 'enter':
                                    editing[3] = False
                                else:
                                    try: funct.savedata[6] = int(str(funct.savedata[6] + typed))
                                    except: pass
                            elif editing[4]:
                                if typed == 'back':
                                    funct.savedata[7] = funct.savedata[7][:-1]
                                elif typed == 'enter':
                                    editing[4] = False
                                else:
                                    funct.savedata[7] += typed
                elif screen == 2:
                    """Inventory"""
                    if sub__screen == 0:
                        "Skins"
                    elif sub__screen == 1:
                        "Invetory"
                    elif sub__screen == 2:
                        "Cases"
                    elif sub__screen == 3:
                        "Perks"
            pygame.display.flip()
if __name__ == "__main__":
    #Saves are saved as follows: Music Volume, SFX Folume, Fullscreen T/F, hostIP, host port, connect IP, connectport,
    # player name, player money, player XP, player LVL, player perks, player inventory (skins),player inventory (variants,
    #player inventory (cases), weapon purchases
    default_save = [1,1,False,"192.168.1.37",
    10666,'108.228.3.179',10666,
    "Mech",0,0,0,[0,0,0,0],[],[],[],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    if os.path.exists('save'):
        print "save located..."
        savedata = funct.loadsave()
        funct.savedata = savedata
    else:
        savesave(default_save)
        savedata = loadsave()
        funct.savedata = savedata
    menu(0)
