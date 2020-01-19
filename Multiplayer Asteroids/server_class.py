import pygame
import socket
import random
import time
class server(pygame.sprite.Sprite):
    def __init__(self,HOST,PORT):
        pygame.sprite.Sprite.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.setblocking(0)
        print "Server Class Running."

        self.connected_clients = []
        self.player_numbers = []
        self.data = []
        self.player_number = 0
        self.reprint_time = 1000
        self.send_data = ""
        self.global_commands = []

        self.timeouts = []
        
        self.wave = 0
        self.paused = True
        self.justPaused = True
        self.gettime = True
        self.ctime = time.time()
        self.pausetime = 30
        self.clock = 0
        self.won = False
        self.required_asteroids = [10,16,24,36,50,62,78,84,96,124,150,256,512,1024]
        self.killedasteroids = 0
        self.requiredasteroids = 0
    def update(self):
        try:
            self.server.listen(1)
            conn, addr = self.server.accept()
            conn.send(str(self.player_number))
            print self.global_commands
            for i in self.global_commands:
                self.data.append(i)
            
            print "Player" + str(self.player_number) + " has joined the server."
            self.player_numbers.append(self.player_number)
            self.timeouts.append(60)
            self.player_number += 1
            self.handle_connection(conn,addr)
        except:
            None#Returns here while waiting for connection.


        self.process_data()
    def process_data(self):
        self.send_data = ""
        for i in self.connected_clients:
            try:
                recieved = i.recv(8192)
                data = recieved.split(";")
                data.pop()
                new_data = []
                for i in data:
                    if i not in new_data:
                        new_data.append(i)
                        #print "New command:",i
                self.data += new_data
            except:
                None
        #BUGGY AS SHIT, PRESUMED BECAUSE OF CLOCK DIFFERENCES.
        #self.paused = False
                
        if self.paused:
            ctime = self.clock
            if self.gettime:
                self.ctime = time.time()
                self.gettime = False
            self.clock = int(time.time() - self.ctime - self.pausetime)* -1
            if self.clock != ctime:
                if self.clock <= 0:
                    print "BEGIN WAVE"
                    required = self.required_asteroids[self.wave]
                    self.requiredasteroids = required
                    self.wave += 1
                    if self.wave > len(self.required_asteroids)-1:

                        print "They won."
                        self.won = True
                        self.data.append("self.won = True;")

                    else:
                        self.pausetime = 30
                        self.data.append("self.wave = " + str(self.wave) + ";")
                        self.data.append("self.clocktime = 0;")
                        self.data.append("self.requiredasteroids = " + str(required) + ";")
                        self.data.append("self.killedasteroids = 0;")
                        self.global_commands.append("self.requiredasteroids = " + str(required) + ";")
                        
                    self.gettime = True
                    self.paused = False

                else:
                    self.data.append("self.clocktime = " + str(self.clock) + ";")
                
            
        else:
            if self.killedasteroids > self.requiredasteroids - 1:
                self.paused = True
                self.killedasteroids = 0
                for i in self.global_commands:
                    if "self.requiredasteroids = " in i:
                        print "removing",i
                        self.global_commands.remove(i)
        recording = False
        for i in self.data:
            if "<{DROP" in i:
                newi = i.replace("<{DROP","")
                newi = newi .replace("}>","")

                place = self.player_numbers.index(int(newi))
                self.player_numbers.pop(place)
                self.connected_clients.pop(place)
                self.timeouts.pop(place)
                print "Player",newi,"has left the server. (disconnect.)"
                
                #Remove global commands
                playertag = "player" + newi
                global_commands = []
                for i in self.global_commands:
                    if playertag in i:
                        print "Removing",i
                    else:
                        global_commands.append(i)
                self.global_commands = global_commands
                self.data.append("self.remove_player(" + newi + ");")

                
                print "Hosting",len(self.connected_clients),"connection(s)."

                
            elif "{<ENDGLOBALS>}" in i:
                recording = False
            elif recording == True:
                print 'Recording',i
                self.global_commands.append(i)
                if i not in self.send_data:
                    self.send_data += i + "; "
            elif "{<GLOBALS>}" in i:
                recording = True
            elif "self.killedasteroids = " in i:
                exec(i)
                self.send_data += "self.killedasteroids = " + str(self.killedasteroids) + ";"
                
            else:
                if i not in self.send_data:
                    self.send_data += i + "; "

        #SEND DATA
        for i in self.connected_clients:
            try:
                i.send(str(self.send_data))
                place = self.connected_clients.index(i)
                self.timeouts[place] = 60
            except:
                place = self.connected_clients.index(i)
                if self.timeouts[place] > 0:
                    self.timeouts[place] -= 1
                else:
                    newi = self.player_numbers[place]
                    self.player_numbers.pop(place)
                    self.connected_clients.pop(place)
                    self.timeouts.pop(place)
                    print "Player",newi,"has left the server. (connection timed out)"
                    
                    playertag = "player" + str(newi)
                    global_commands = []
                    for i in self.global_commands:
                        if playertag in i:
                            print "Removing",i
                        else:
                            global_commands.append(i)
                    self.global_commands = global_commands

                    self.data.append("self.remove_player(" + str(newi) + ");")  
                    print "Hosting",len(self.connected_clients),"connection(s)."

        self.data = []
    def handle_connection(self,conn,addr):
        self.connected_clients.append(conn)
        print "(Client connected from",addr,")"
        print "Hosting",len(self.connected_clients),"connection(s)."
        
        
