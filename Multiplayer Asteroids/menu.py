import pygame
pygame.mixer.init()
import images
import skin_names
import run_client
import run_server
import random
import sounds
import math
import client_globals
def textbox(screen,text,color,(x,y),font):
    """Text to be displayed, color (RGB), position, font size. -> Rect"""
    text = font.render(text,255,color)
    screen.blit(text,(x*client_globals.global_multiplier,y*client_globals.global_multiplier))

    text_size = text.get_size()
    return pygame.rect.Rect(x*client_globals.global_multiplier,y*client_globals.global_multiplier,text_size[0],text_size[1])

def casebox(screen,number,(x,y)):
    image = images.cases[number]
    screen.blit(image,(x,y))
    return pygame.rect.Rect(x,y,50,50)
def skinbox(screen,grade,number,(x,y)):
    skins = images.case0 + images.case1
    screen.blit(pygame.transform.scale(images.rarities[grade],(50,50)),(x,y))
    image = skins[number]
    screen.blit(image,(x,y))
    return pygame.rect.Rect(x,y,50,50)
def opencase(screen,number):
    background = screen.copy()

    case0 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    case1 = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
    composition = []
    for i in range(0,28):
        grade = random.randint(0,1000)
        if grade >= 0 and grade < 700:
            skin = random.randint(0,6) #Common
        elif grade >= 700 and grade < 850:
            skin = random.randint(7,11) #Uncommon
        elif grade >= 850 and grade < 900:
            skin = random.randint(12,14) #Rare
        elif grade >= 900 and grade < 975:
            skin = random.randint(15,16) #Covert
        elif grade >= 975 and grade < 1001:
            skin = 17 #Legendary
        composition.append(skin)
    grade = random.randint(0,1000)
    if grade >= 0 and grade < 700:
        officialskin = random.randint(0,6) #Common
    elif grade >= 700 and grade < 850:
        officialskin = random.randint(7,11) #Uncommon
    elif grade >= 850 and grade < 900:
        officialskin = random.randint(12,14) #Rare
    elif grade >= 900 and grade < 975:
        officialskin = random.randint(15,16) #Covert
    elif grade >= 975 and grade < 1001:
        officialskin = 17 #Legendary
    composition.append(officialskin)
    for i in range(0,28):
        grade = random.randint(0,1000)
        if grade >= 0 and grade < 700:
            skin = random.randint(0,6) #Common
        elif grade >= 700 and grade < 850:
            skin = random.randint(7,11) #Uncommon
        elif grade >= 850 and grade < 900:
            skin = random.randint(12,14) #Rare
        elif grade >= 900 and grade < 975:
            skin = random.randint(15,16) #Covert
        elif grade >= 975 and grade < 1001:
            skin = 17 #Legendary
        composition.append(skin)
    if number == 0:
        print "Unboxed",number,"and recieved",case0[officialskin]
    if number == 1:
        print "Unboxed",number,"and recieved",case1[officialskin]
    scroll_position = -50 * 56
    speed = 25.0
    second_speed = 1.0001
    
    reel = images.reel
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pressed = True
        offset = 0
        screen.blit(background,(0,0))
        screen.blit(reel,(40,140))
        #reel = images.reel
        if number == 0:
            
            for i in composition:
                if i >= 0 and i < 7:
                    screen.blit(images.rarities[0],(scroll_position - offset,145))
                elif i >= 7 and i < 12:
                    screen.blit(images.rarities[1],(scroll_position - offset,145))
                elif i >= 12 and i < 15:
                    screen.blit(images.rarities[2],(scroll_position - offset,145))
                elif i >= 15 and i < 17:
                    screen.blit(images.rarities[3],(scroll_position - offset,145))
                elif i == 17:
                    screen.blit(images.rarities[4],(scroll_position - offset,145))
                screen.blit(images.case0[i],(scroll_position - offset,145))
                offset -= 50
                
            if scroll_position < 0:
                scroll_position += speed
                if speed > 0.1:

                    speed = speed -  0.1
                    #speed -= second_speed
                else:
                    speed = 0.1
                print speed
            else:
                return case0[officialskin]
        if number == 1:
            for i in composition:
                if i >= 0 and i < 7:
                    screen.blit(images.rarities[0],(scroll_position - offset,145))
                elif i >= 7 and i < 12:
                    screen.blit(images.rarities[1],(scroll_position - offset,145))
                elif i >= 12 and i < 15:
                    screen.blit(images.rarities[2],(scroll_position - offset,145))
                elif i >= 15 and i < 17:
                    screen.blit(images.rarities[3],(scroll_position - offset,145))
                elif i == 17:
                    screen.blit(images.rarities[4],(scroll_position - offset,145))
                screen.blit(images.case1[i],(scroll_position - offset,145))
                offset -= 50
            if scroll_position < 0:
                scroll_position += speed
                if speed > 0.5:
                    speed -= 0.01
            else:
                return case1[officialskin]
        sidebar_left = pygame.draw.rect(screen,(100,100,100),(0,140,50,70))
        sidebar_right = pygame.draw.rect(screen,(100,100,100),(750,140,50,70))
        pygame.display.flip()
        
def Run():

    #Get settings.
    #HOST_IP
    #HOST_PORT
    #CLIENT_IP
    #CLIENT_PORT

    pygame.font.init()

    fileio = open("settings",'r')
    for i in fileio.readlines():
        exec(i)
    fileio.close()

    resolutionsx = [320,640,800,1024,1280,1600,1920]
    resolutionsy = [240,480,600,768,960,1200,1080]
    scale_factors = [0.4,0.8,1,1.28,1.6,2,2.4]
    if fullscreen:
        d = pygame.display.set_mode((resolutionsx[selected_resolution],resolutionsy[selected_resolution]),pygame.FULLSCREEN)
    else:
        d = pygame.display.set_mode((resolutionsx[selected_resolution],resolutionsy[selected_resolution]))
    last_resolution = selected_resolution
    client_globals.global_multiplier = scale_factors[selected_resolution]
    title_font = pygame.font.SysFont(None,int(80*client_globals.global_multiplier))
    semi_font = pygame.font.SysFont(None,int(40*client_globals.global_multiplier))
    caption_font = pygame.font.SysFont(None,int(20*client_globals.global_multiplier))
    menu = "Main"
    sub_menu = "Main"
    pressed = True

    title = title_font.render("Asteroids! MP",255,(255,255,255))

    title1 = semi_font.render("Play (Connect)",255,(255,255,255))
    title2 = semi_font.render("Play (Host)",255,(255,255,255))
    title3 = semi_font.render("Settings",255,(255,255,255))
    title4 = semi_font.render("Exit",255,(255,255,255))

    playSound = 0

    pygame.mouse.set_visible(1)


    music = sounds.menu_song.play()


    images.load_images(client_globals.global_multiplier)
    editing = 0
    Version = str(version)
    typespeed = 30
    in_cases_menu = False
    in_skins_menu = False

    while True:
        d.fill((0,0,0))
        d.blit(images.background,(0,0))
        textbox(d,"V"+Version,(255,255,255),(760,580),caption_font)
        mousepos = pygame.mouse.get_pos()
        mouse = pygame.rect.Rect(mousepos[0],mousepos[1],1,1)
        pressed = False
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pressed = True

        if menu == "Main":
            title0_rect = textbox(d,"Asteroids! MP",(200,200,200),(200,20),title_font)
            title1_rect = textbox(d,"Play!",(200,200,200),(350,100),semi_font)
            title2_rect = textbox(d,"Host",(200,200,200),(350,130),semi_font)
            title3_rect = textbox(d,"Settings",(200,200,200),(320,160),semi_font)
            title4_rect = textbox(d,"Exit",(200,200,200),(350,190),semi_font)
            if mouse.colliderect(title1_rect):
                if playSound:
                    sounds.click.play()
                    playSound = 0
                title1_rect = textbox(d,"Play!",(0,200,0),(350,100),semi_font)
                if pressed:
                    sounds.purchased.play()
                    d.fill((0,0,0))
                    Connecting = title_font.render("Connecting...",255,(255,255,255))
                    d.blit(Connecting,(200,20))
                    pygame.display.flip()
                    music.stop()
                    run_client.Run()
                    break
            elif mouse.colliderect(title2_rect):
                if playSound:
                    sounds.click.play()
                    playSound = 0
                title2_rect = textbox(d,"Host",(255,255,255),(350,130),semi_font)
                if pressed:
                    sounds.purchased.play()
                    pygame.display.quit()
                    pygame.mixer.quit()
                    run_server.Run()
                    break
            elif mouse.colliderect(title3_rect):
                if playSound:
                    sounds.click.play()
                    playSound = 0
                title3_rect = textbox(d,"Settings",(255,255,255),(320,160),semi_font)
                if pressed:
                    sounds.purchased.play()
                    menu = "Settings"
            elif mouse.colliderect(title4_rect):
                if playSound:
                    sounds.click.play()
                    playSound = 0
                title4_rect = textbox(d,"Exit",(255,255,255),(350,190),semi_font)
                if pressed:
                    sounds.purchased.play()
                    pygame.display.quit()
                    break
            else:
                playSound = 1
        elif menu == "Settings":
            if sub_menu == "Main":
                title0_rect = textbox(d,"Asteroids Settings",(255,255,255),(150,20),title_font)
                title1_rect = textbox(d,"Multiplayer",(200,200,200),(310,100),semi_font)
                title2_rect = textbox(d,"Player",(200,200,200),(340,130),semi_font)
                title3_rect = textbox(d,"Game",(200,200,200),(350,160),semi_font)
                title4_rect = textbox(d,"Back",(200,200,200),(350,190),semi_font)
                if mouse.colliderect(title1_rect):
                    title1_rect = textbox(d,"Multiplayer",(255,255,255),(310,100),semi_font)
                    if pressed:
                       sub_menu = "Multiplayer"

                elif mouse.colliderect(title2_rect):
                    title2_rect = textbox(d,"Player",(255,255,255),(340,130),semi_font)
                    if pressed:
                       sub_menu = "Player"

                elif mouse.colliderect(title3_rect):
                    title3_rect = textbox(d,"Game",(255,255,255),(350,160),semi_font)
                    if pressed:
                       sub_menu = "Game"

                elif mouse.colliderect(title4_rect):
                    title3_rect = textbox(d,"Back",(255,255,255),(350,190),semi_font)
                    if pressed:
                       menu = "Main"

                       fileio = open("settings",'w')
                       fileio.write("print 'IMPORTING SETTINGS, DO NOT MODIFY THIS FILE.'\nHOST_IP = '" + HOST_IP + "'\nHOST_PORT = '" + HOST_PORT + "'\nCLIENT_IP = '" + CLIENT_IP +\
                                    "'\nCLIENT_PORT = '" + CLIENT_PORT + "'\nversion = " + str(version) + "\nNAME = '" + NAME + "'\nfullscreen = " + str(fullscreen) +\
                                    "\nselected_resolution = " + str(selected_resolution) + "\nSKINS = " +str(SKINS) + "\nCASES = " + str(CASES) + "\nselected_skin = " + str(selected_skin))
                       fileio.close()
                                    


            elif sub_menu == "Multiplayer":
                title = title_font.render("Multiplayer Settings",255,(255,255,255))
                title1 = semi_font.render("Connect IP",255,(255,255,255))
                title2 = semi_font.render("Connect PORT",255,(255,255,255))
                title3 = semi_font.render("Host IP",255,(255,255,255))
                title4 = semi_font.render("Host PORT",255,(255,255,255))
                title1_rect = textbox(d,CLIENT_IP,(200,200,200),(310,100),semi_font)
                title2_rect = textbox(d,str(CLIENT_PORT),(200,200,200),(310,130),semi_font)
                title3_rect = textbox(d,HOST_IP,(200,200,200),(310,160),semi_font)
                title4_rect = textbox(d,str(HOST_PORT),(200,200,200),(310,190),semi_font)
                title5_rect = textbox(d,"Back",(200,200,200),(350,250),semi_font)
                
                if mouse.colliderect(title1_rect):
                    title1_rect = textbox(d,CLIENT_IP,(255,255,255),(310,100),semi_font)
                    if pressed:
                        editing = 1
                if mouse.colliderect(title2_rect):
                    title2_rect = textbox(d,str(CLIENT_PORT),(255,255,255),(310,130),semi_font)
                    if pressed:
                        editing = 2
                if mouse.colliderect(title3_rect):
                    title3_rect = textbox(d,HOST_IP,(255,255,255),(310,160),semi_font)
                    if pressed:
                        editing = 3
                if mouse.colliderect(title4_rect):
                    title4_rect = textbox(d,str(HOST_PORT),(255,255,255),(310,190),semi_font)
                    if pressed:
                        editing = 4
                if mouse.colliderect(title5_rect):
                    title5_rect = textbox(d,"Back",(255,255,255),(350,250),semi_font)
                    if pressed:
                       sub_menu = "Main"
                key = pygame.key.get_pressed()
                back = 0
                shift = 0
                typespeed -= 1
                if typespeed < 0:
                    if 1 in key:
                        if key[pygame.K_RETURN]:
                            editing = 0
                        elif key[pygame.K_BACKSPACE]:
                            typespeed = 20
                            back = 1
                        elif key[pygame.K_LSHIFT]:
                            shift = 1

                        if editing == 1:
                            if back == 1:
                                CLIENT_IP = CLIENT_IP[:-1]
                            else:
                                try:
                                    if shift == 1:
                                        CLIENT_IP += chr(key.index(1)).upper()
                                    else:
                                        CLIENT_IP += chr(key.index(1))
                                    typespeed = 20
                                except Exception as error:
                                    print error
                        if editing == 2:
                            if back == 1:
                                CLIENT_PORT = CLIENT_PORT[:-1]
                            else:
                                try:
                                    if shift == 1:
                                        CLIENT_PORT += chr(key.index(1)).upper()
                                    else:
                                        CLIENT_PORT += chr(key.index(1))
                                    typespeed = 20
                                except Exception as error:
                                    print error
                        if editing == 3:
                            if back == 1:
                                HOST_IP = HOST_IP[:-1]
                            else:
                                try:
                                    if shift == 1:
                                        HOST_IP += chr(key.index(1)).upper()
                                    else:
                                        HOST_IP += chr(key.index(1))
                                    typespeed = 20
                                except Exception as error:
                                    print error
                        if editing == 4:
                            if back == 1:
                                HOST_PORT = HOST_PORT[:-1]
                            else:
                                try:
                                    if shift == 1:
                                        HOST_PORT += chr(key.index(1)).upper()
                                    else:
                                        HOST_PORT += chr(key.index(1))
                                    typespeed = 20
                                except Exception as error:
                                    print error
                                    
                d.blit(title1,(50,100))
                d.blit(title2,(50,130))
                d.blit(title3,(50,160))
                d.blit(title4,(50,190))
                


            elif sub_menu == "Player":
                if in_cases_menu:
                    title1 = semi_font.render("Cases",255,(255,255,255))
                    d.blit(images.case_background,(144,44))
                    posx = 145
                    posy = 44
                    positionx = 0
                    positiony = 0
                    for i in CASES:
                        if positionx > 9:
                            positionx = 0
                            positiony += 1
                        x = 51 * positionx + posx
                        y = 51 * positiony + posy
                        box = casebox(d,i,(x,y))
                        if mouse.colliderect(box):
                            if pressed:
                                newskin = opencase(d,i)
                                SKINS.append(newskin)
                                CASES.remove(i)
                                fileio = open("settings",'w')
                                fileio.write("print 'IMPORTING SETTINGS, DO NOT MODIFY THIS FILE.'\nHOST_IP = '" + HOST_IP + "'\nHOST_PORT = '" + HOST_PORT + "'\nCLIENT_IP = '" + CLIENT_IP +\
                                            "'\nCLIENT_PORT = '" + CLIENT_PORT + "'\nversion = " + str(version) + "\nNAME = '" + NAME + "'\nfullscreen = " + str(fullscreen) +\
                                            "\nselected_resolution = " + str(selected_resolution) + "\nSKINS = " +str(SKINS) + "\nCASES = " + str(CASES) + "\nselected_skin = " + str(selected_skin))
                                fileio.close()

                                in_cases_menu = False
                                in_skins_menu = True
                                
                        positionx += 1
                    back = textbox(d,"Back",(200,200,200),(10,560),semi_font)
                    if mouse.colliderect(back):
                        back = textbox(d,"Back",(255,255,255),(10,560),semi_font)
                        if pressed:
                            in_cases_menu = False
                    
  

                elif in_skins_menu:
                    blue_skins = [0,1,2,3,4,5,6,18,19,20,21,22,23,24]
                    purple_skins = [7,8,9,10,11,25,26,27,28,29]
                    pink_skins = [12,13,14,30,31,32]
                    red_skins = [15,16,33,34]
                    yellow_skins = [17,35]
                    title1 = semi_font.render("Skins",255,(255,255,255))
                    d.blit(images.case_background,(144,44))
                    posx = 145
                    posy = 45
                    index = 0
                    positionx = 0
                    positiony = 0
                    hover = -1
                    for i in SKINS:
                        if positionx > 9:
                            positionx = 0
                            positiony += 1
                        x = 51 * positionx + posx
                        y = 51 * positiony + posy
                        if i in blue_skins:
                            box = skinbox(d,0,i,(x,y))
                        elif i in purple_skins:
                            box = skinbox(d,1,i,(x,y))
                        elif i in pink_skins:
                            box = skinbox(d,2,i,(x,y))
                        elif i in red_skins:
                            box = skinbox(d,3,i,(x,y))
                        elif i in yellow_skins:
                            box = skinbox(d,4,i,(x,y))
                        if index == selected_skin:
                            d.blit(images.selected,(x-1,y-1))
                        if mouse.colliderect(box):
                            hover = i
                            if pressed:
                                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                    SKINS.pop(index)
                                else:
                                    selected_skin = index#SKINS.index(i)

                        positionx += 1
                        index += 1
                    if hover != -1:
                        textbox(d,skin_names.skin_names[hover],(255,255,255),(mousepos[0],mousepos[1]),caption_font)
                    back = textbox(d,"Back",(200,200,200),(10,560),semi_font)
                    if mouse.colliderect(back):
                        back = textbox(d,"Back",(255,255,255),(10,560),semi_font)
                        if pressed:
                            in_skins_menu = False
  

                else:
                    title0_rect = textbox(d,"Player Settings",(255,255,255),(150,20),title_font)
                    title1 = semi_font.render("Name",255,(255,255,255))
                    title1_rect = textbox(d,NAME,(200,200,200),(350,100),semi_font)
                    title2_rect = textbox(d,"Skins",(200,200,200),(345,130),semi_font)
                    title3_rect = textbox(d,"Cases",(200,200,200),(345,160),semi_font)
                    title4_rect = textbox(d,"Back",(200,200,200),(350,190),semi_font)

                    if mouse.colliderect(title1_rect):
                        title1_rect = textbox(d,NAME,(255,255,255),(350,100),semi_font)
                        if pressed:
                            editing = 1
                    if mouse.colliderect(title2_rect):
                        title2_rect = textbox(d,"Skins",(255,255,255),(345,130),semi_font)
                        if pressed:
                            in_skins_menu = True
                    if mouse.colliderect(title3_rect):
                        title3_rect = textbox(d,"Cases",(255,255,255),(345,160),semi_font)
                        if pressed:
                            in_cases_menu = True

                    if mouse.colliderect(title4_rect):
                        title3_rect = textbox(d,"Back",(255,255,255),(350,190),semi_font)
                        if pressed:
                           sub_menu = "Main"




                    key = pygame.key.get_pressed()


                    back = 0
                    shift = 0
                    typespeed -= 1
                    if typespeed < 0:
                        if 1 in key:
                            if key[pygame.K_RETURN]:
                                editing = 0
                            elif key[pygame.K_BACKSPACE]:
                                back = 1
                                typespeed = 20
                            elif key[pygame.K_LSHIFT]:
                                shift = 1

                            if editing == 1:
                                if back == 1:
                                    NAME = NAME[:-1]
                                else:
                                    try:
                                        if shift == 1:
                                            NAME += chr(key.index(1)).upper()
                                        else:
                                            NAME += chr(key.index(1))
                                        typespeed = 20
                                    except Exception as error:
                                        print error
                d.blit(title1,(50,100))
            elif sub_menu == "Game":
                title0_rect = textbox(d,"Game Settings",(255,255,255),(150,20),title_font)
                title1 = semi_font.render("Resolution",255,(255,255,255))
                title2 = semi_font.render("Fullscreen",255,(255,255,255))
                descg = (selected_resolution * 0.25) + 0.5
                title1_rect = textbox(d,str(resolutionsx[selected_resolution]) + "x" + str(resolutionsy[selected_resolution]) + " (x" + str(descg) + ")",(200,200,200),(350,100),semi_font)
                title2_rect = textbox(d,str(fullscreen),(200,200,200),(345,130),semi_font)
                title3_rect = textbox(d,"---",(200,200,200),(345,160),semi_font)
                title4_rect = textbox(d,"Back",(200,200,200),(350,190),semi_font)
                if mouse.colliderect(title1_rect):
                    title1_rect = textbox(d,str(resolutionsx[selected_resolution]) + "x" + str(resolutionsy[selected_resolution]),(255,255,255),(350,100),semi_font)
                    if pressed:
                        last_resolution = selected_resolution
                        selected_resolution += 1
                        if selected_resolution == len(resolutionsx):
                            selected_resolution = 0
                if mouse.colliderect(title2_rect):
                    title2_rect = textbox(d,str(fullscreen),(255,255,255),(345,130),semi_font)
                    if pressed:
                        if fullscreen:
                            fullscreen = False
                            d = pygame.display.set_mode((resolutionsx[selected_resolution],resolutionsy[selected_resolution]))
                        else:
                            fullscreen = True
                            d = pygame.display.set_mode((resolutionsx[selected_resolution],resolutionsy[selected_resolution]),pygame.FULLSCREEN)
                if mouse.colliderect(title3_rect):
                    title3_rect = textbox(d,"---",(255,255,255),(345,160),semi_font)

                if mouse.colliderect(title4_rect):
                    title3_rect = textbox(d,"Back",(255,255,255),(350,190),semi_font)
                    if pressed:
                        if last_resolution != selected_resolution:
                            client_globals.global_multiplier = scale_factors[selected_resolution]
                            d = pygame.display.set_mode((resolutionsx[selected_resolution],resolutionsy[selected_resolution]))
                            images.load_images(client_globals.global_multiplier)
                            title_font = pygame.font.SysFont(None,int(80*client_globals.global_multiplier))
                            semi_font = pygame.font.SysFont(None,int(40*client_globals.global_multiplier))
                            caption_font = pygame.font.SysFont(None,int(20*client_globals.global_multiplier))

                        fileio = open("settings",'w')
                        fileio.write("print 'IMPORTING SETTINGS, DO NOT MODIFY THIS FILE.'\nHOST_IP = '" + HOST_IP + "'\nHOST_PORT = '" + HOST_PORT + "'\nCLIENT_IP = '" + CLIENT_IP +\
                                    "'\nCLIENT_PORT = '" + CLIENT_PORT + "'\nversion = " + str(version) + "\nNAME = '" + NAME + "'\nfullscreen = " + str(fullscreen) +\
                                    "\nselected_resolution = " + str(selected_resolution) + "\nSKINS = " +str(SKINS) + "\nCASES = " + str(CASES) + "\nselected_skin = " + str(selected_skin))
                        fileio.close()
                        sub_menu = "Main"
                d.blit(title1,(50,100))
                d.blit(title2,(50,130))
        pygame.display.flip()

