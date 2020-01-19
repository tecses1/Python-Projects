import pygame
import socket
import server_class
import menu
def Run():
    print "Preparing loop..."
    
    fileio = open("settings",'r')
    for i in fileio.readlines():
        exec(i)
    fileio.close()
    
    Hosting_server = True

    server_container = pygame.sprite.GroupSingle()
    try:
        PORT = int(HOST_PORT)
    except:
        print "Invalid server information."
        Hosting_server = False
        menu.Run()
        
    server_container.add(server_class.server(HOST_IP,PORT))
    clock = pygame.time.Clock()
    while Hosting_server:
        for i in server_container:
            if i.won:
                i.kill()
                Hosting_server = False
                menu.Run()

        server_container.update()
            
