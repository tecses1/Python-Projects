import pygame
import socket
import server_class
import client_class
import images
import menu
import random
def Run():

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

    client = pygame.sprite.GroupSingle()

    
    client.add(client_class.client(d,CLIENT_IP,int(CLIENT_PORT),client))
    running = True
    clock = pygame.time.Clock()
    position = 0
    pygame.mouse.set_visible(0)
    won = False
    while running == 1:
        d.fill((0,0,0))
        #d.blit(images.background,(position,0))
        #d.blit(images.background,(800 + position,0))
        position -= 1
        if position <= -800:
            position = 0
        clock.tick(60)
        
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    for client in client:
                        client.connected.sendall("<{DROP" + str(client.player_number) + "}>;")
                    running = False
        for i in client:
            won = i.won
            if won:
                i.kill()
        client.update() 
        try:
            if len(client) == 0:
                print "GAME OVER."
                background = d.copy()
                running = 2   
        except:
            print "GAME OVER."
            background = d.copy()
            running = 2

            
        pygame.display.flip()
    while running == 2:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if won:
                        fileio = open("settings",'r')
                        for i in fileio.readlines():
                            exec(i)
                        fileio.close()
                        CASES.append(random.randint(0,1))
                        fileio = open("settings",'w')
                        fileio.write("print 'IMPORTING SETTINGS, DO NOT MODIFY THIS FILE.'\nHOST_IP = '" + HOST_IP + "'\nHOST_PORT = '" + HOST_PORT + "'\nCLIENT_IP = '" + CLIENT_IP +\
                                    "'\nCLIENT_PORT = '" + CLIENT_PORT + "'\nversion = " + str(version) + "\nNAME = '" + NAME + "'\nfullscreen = " + str(fullscreen) +\
                                    "\nselected_resolution = " + str(selected_resolution) + "\nSKINS = " +str(SKINS) + "\nCASES = " + str(CASES) + "\nselected_skin = " + str(selected_skin))
                        fileio.close()
                    running = 0
                    menu.Run()
        d.blit(background,(0,0))
        if won:
            d.blit(images.won,(0,0))
        else:
            d.blit(images.death,(0,0))
        pygame.display.flip()
