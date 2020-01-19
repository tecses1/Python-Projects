import socket
import pygame
import ast
import random
import images
import time
import menu
from funct import *
class Server():
    def __init__(self,(host,port)):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print "binding to",host,port
        self.socket.bind((host,port))
        self.socket.listen(10)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.connections = []
        self.ids = []
        self.addresses = []

        self.alienstokill = 0
        self.alienID = 0
        self.wspawntime = 30000
        self.spawntime = 2500
        self.cooldown = 30000
        self.input = ""
        self.inarow = 0
        self.socket.setblocking(0)
    def sendtoallconn(self,data):
        for i in self.connections:
            if i != None:
                try:
                    i.send(data)
                    
                except socket.error, e:
                    print e
    def update(self):
        #Accept new connections
        skip_update = False
        try:
            conn, addr = self.socket.accept()

            self.connections.append(conn)
            conn.sendall(str(self.connections.index(conn)))
            self.ids.append(self.connections.index(conn))
            self.sendtoallconn("{NPU}=" + str(self.ids)+"|")
            print self.ids
            self.addresses.append(addr)
        except socket.error, err:
            #If no new connections exist-> ignore that shit
            pass
        #if len([x for x in self.connections if x != None]) > 0:
        if len(self.connections) > 0:
            self.cooldown -= 1
            if self.cooldown < 2 and self.cooldown > 0:
                self.alienstokill = 100
            if self.spawntime > 0:
                self.spawntime -= 1
            else:
                rl = random.randint(0,1)
                tb = random.randint(0,1)
                if rl == 0:
                    x = random.randint(800*2,800*3)
                if rl == 1:
                    x = random.randint(-800*3,-800*2)
                if tb == 0:
                    y = random.randint(-800*3,-800*2)
                if tb == 1:
                    y = random.randint(800*2,800*3)

                self.alienID += 1
                self.input += "{SE}(" + str(x)+"," +str(y)+","+str(self.alienID)+",5,5,5)|"
                self.spawntime = self.wspawntime
        if self.alienstokill > 0:
            self.input += "T|"
        else:
            self.input += "F|"
        for i in self.connections:
            if i != None:
                try:
                    data = i.recv(8192*4).split("|")
                    data = data[0:len(data)-1]
                    for x in data:
                        if x not in self.input:
                            if x != "":
                                self.input += x + "|"
                    self.inarow = 0
                except socket.error, e:
                    if str(e).startswith("[Errno 10035]"):
                        self.inarow += 1
                        if self.inarow >= 25000:
                            print "Player",self.connections.index(i)," connection lost. (PL)"
                            self.ids[self.connections.index(i)] = str(self.ids[self.connections.index(i)])
                            self.connections[self.connections.index(i)] = None
                            self.sendtoallconn("{NPU}=" + str(self.ids)+"|")
                            i.close()

                        #print "Lost connection from client... Waiting for reconnection."
                    elif str(e).startswith("[Errno 104"):
                        print "Player",self.connections.index(i),"disconnected."
                        self.ids[self.connections.index(i)] = str(self.ids[self.connections.index(i)])
                        self.connections[self.connections.index(i)] = None
                        self.sendtoallconn("{NPU}=" + str(self.ids)+"|")
                        i.close()
                        
                    else:
                        print e
                        self.ids[self.connections.index(i)] = str(self.ids[self.connections.index(i)])
                        self.connections[self.connections.index(i)] = None
                        self.sendtoallconn("{NPU}=" + str(self.ids)+"|")
                        i.close()
        self.sendtoallconn(self.input)
        self.input = ""

class Client():
    def __init__(self,(host,port)):
        tries = 8
        display = pygame.display.set_mode((800,600))
        font = pygame.font.SysFont(None,30)
        imageframe = 0
        connecting = 1
        
        animframe = 0
        animtime = 3
        time_to_try = 0
        while connecting == 1:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        connecting = 0
            display.blit(images.splash[3],(0,0))
            fontBox(display,font,"Connecting...",(620,200))
            display.blit(images.wheel[animframe],(750,550))
            pygame.display.flip()
            animtime -= 1
            if animtime <= 0:
                animtime = 3
                animframe += 1
                time_to_try += 1
                if animframe > 49:
                    animframe = 0
                if time_to_try >= 30:
                    try:
                        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        self.socket.connect((host,port))
                        id_string = self.socket.recv(2).replace("{","")
                        self.uniqueID = int(id_string)
                        connecting = 2
                    except socket.error:
                        tries -= 1
                        if tries <= 0:
                            connecting = 0
                    time_to_try = 0
        if connecting == 0:
            display.blit(images.splash[3],(0,0))
            fontBox(display,font,"Failed to connect!",(620,190))
            pygame.display.flip()
            time.sleep(3)
            menu.menu(1)
        self.commandstp = []
        self.inarow = 0
        self.socket.setblocking(0)
    def recvServer(self):
        try:
            data = self.socket.recv(8192).split("|")
            data = data[0:len(data)-1]
            for x in data:
                if x not in self.commandstp:
                    if x != "":
                        self.commandstp.append(x)
            self.inarow = 0
            return True
        except socket.error, e:
            if str(e).startswith("[Errno 10035]"):
                self.inarow += 1
                if self.inarow >= 10 and self.inarow < 100:
                    if self.inarow == 10:
                        print "Packet loss detected..."
                elif self.inarow >= 100 and self.inarow < 3000:
                    if self.inarow == 100:
                        print "Extreme Packet loss detected..."
                elif self.inarow >= 3000:
                    print "connection lost."
                    self.socket.close()
                    
            return False

    def getData(self):
        yeet = self.commandstp
        self.commandstp = []
        return yeet
    def send_updates(self,update):
        try:
            self.socket.sendall(update)
        except socket.error, e:
            pass
