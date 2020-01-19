import pygame
pygame.mixer.init()
import socket
import server_class
import client_class
import images
import client_globals
import math
import random
import sounds
class shot(pygame.sprite.Sprite):
    def __init__(self,owner,screen,(posw,posh),(endposw,endposh)):
        pygame.sprite.Sprite.__init__(self)
        posw = posw + client_globals.offsetx
        posh = posh + client_globals.offsety
        #print endposw,endposh
        endposw = endposw + client_globals.offsetx
        endposh = endposh + client_globals.offsety
        
        self.start_pos = (posw,posh)
        self.end_pos = (endposw,endposh)
        self.screen = screen
        sounds.laser_shot.play()
        self.lifetime = 3
        
        self.owner = owner
        self.rect = pygame.rect.Rect(self.end_pos[0],self.end_pos[1],5,5)
        
    def update(self):
        self.rect = pygame.rect.Rect(self.end_pos[0],self.end_pos[1],5,5)
        pygame.draw.line(self.screen,(255,255,255),self.start_pos,self.end_pos,2)
        self.lifetime -= 1
        if self.lifetime < 0:
            self.kill()
class asteroid(pygame.sprite.Sprite):
    def __init__(self,screen,(posw,posh),(speedw,speedh),atype):
        pygame.sprite.Sprite.__init__(self)
        self.posw = posw
        self.posh = posh
        self.speedw = float(speedw) / 10
        self.speedh = float(speedh) / 10
        self.screen = screen
        

        self.image = images.asteroid1
        self.hp = 2
        if atype <= 50:
            self.image = images.asteroid1
            self.hp = 2
            self.tier = 1

        elif atype > 50 and atype <= 75:
            self.image = images.asteroid2
            self.hp = 4
            self.tier = 2
        elif atype >75 and atype <= 85:
            self.image = images.asteroid3
            self.hp = 8
            self.tier = 3
        elif atype > 85 and atype <= 95:
            self.image = images.asteroid4
            self.hp = 16
            self.tier = 4
        elif atype > 95 and atype <= 100:
            self.hp = 24
            self.tier = 5
            self.image = images.asteroid5
        self.maxhp = self.hp
        self.justDied = 0
        self.killedby = -1
        self.frame = 0
        self.animtime = 5
    def update(self):

        #self.rect = pygame.draw.rect(self.screen,(255,255,255),(self.posw,self.posh,50,50))

        if self.posw < -100 or self.posw > self.screen.get_size()[0] * 2 + 50:
            self.kill()
        if self.posh < -100 or self.posh > self.screen.get_size()[1] * 2 + 50:
            self.kill()
        if self.hp <= 0:
            if self.justDied == 0:
                sounds.asteroid_death.play()
                self.justDied = 1
            self.die()
            self.rect = pygame.rect.Rect(self.posw,self.posh,0,0)
        else:
            self.rect = pygame.rect.Rect(self.posw+client_globals.offsetx,self.posh+client_globals.offsety,40,40)
        self.posw += self.speedw
        self.posh += self.speedh
        if self.hp < self.maxhp and self.hp > 0:
            healthbar_red = pygame.draw.rect(self.screen,(200,0,0),(self.posw+client_globals.offsetx, self.posh+client_globals.offsety+50,50,5))
            healthbar_green = pygame.draw.rect(self.screen,(0,200,0),(self.posw+client_globals.offsetx, self.posh+client_globals.offsety+50,self.hp * 50 / self.maxhp,5))
        self.screen.blit(self.image,(self.posw+client_globals.offsetx,self.posh+client_globals.offsety))
    def die(self):
        self.animtime -= 1
        if self.animtime < 0:
            self.image = images.explosion_anim[self.frame]
            self.frame+= 1
            if self.frame >= len(images.explosion_anim):
                self.kill()
class player(pygame.sprite.Sprite):
    def __init__(self,screen,playernumber,(posw,posh)):
        pygame.sprite.Sprite.__init__(self)
        self.posw = posw
        self.posh = posh
        self.screen = screen
        self.player_number = playernumber

        self.angle = 0
        self.spawntime = 180
        self.font3 = pygame.font.SysFont(None,15)
        self.rect = pygame.rect.Rect(self.posw,self.posh,30,30)
        self.skins = images.case0 + images.case1
    def update(self):
        try:
            exec("self.posw = client_globals.player" + str(self.player_number) + "_position_x")
            exec("self.posh = client_globals.player" + str(self.player_number) + "_position_y")
            exec("self.angle = client_globals.player" + str(self.player_number) + "_angle")
            exec("self.hp = client_globals.player" + str(self.player_number) + "_hp")
            exec("self.hpmultiplier = client_globals.player" + str(self.player_number) + "_hpmultiplier")
            exec("self.kills = client_globals.player" + str(self.player_number) + "_kills")
            exec("self.name = client_globals.player" + str(self.player_number) + "_name")
            exec("self.money = client_globals.player" + str(self.player_number) + "_money")
            exec("self.skin = client_globals.player" + str(self.player_number) + "_skin")
            self.image = self.skins[self.skin]
        except:
            print "Error processing information."
        #self.rect = pygame.draw.rect(self.screen,(255,255,255),(self.posw,self.posh,10,10))
        self.posw = self.posw + client_globals.offsetx
        self.posh = self.posh + client_globals.offsety
        #print "Player",self.player_number,"global coordinates:",self.posw,self.posh
        rotimage = pygame.transform.rotate(self.image,self.angle)
        rect = rotimage.get_rect(center=(self.posw,self.posh))
        self.rect = pygame.rect.Rect(self.posw,self.posh,30,30)
        self.screen.blit(rotimage,rect)
        #if self.posw < self.screen.get_size()[0]:
        #    print "Off screen left"
        #if self.posw > self.screen.get_size()[0]:
        #
        #if self.posh < self.screen.get_size()[1]:
        #
        #if self.posh > self.screen.get_size()[1]:
        healthbar_red = pygame.draw.rect(self.screen,(200,0,0),(self.posw-20, self.posh+20,50,10))
        healthbar_green = pygame.draw.rect(self.screen,(0,200,0),(self.posw-20, self.posh+20,self.hp * 50 / self.hpmultiplier,10))

        name_display = self.font3.render(self.name,255,(255,255,255))
        self.screen.blit(name_display,(self.posw-20,self.posh+20))
class client(pygame.sprite.Sprite):
    def __init__(self,screen,HOST,PORT,parentgroup):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        fileio = open("settings",'r')
        for i in fileio.readlines():
            exec(i)
        fileio.close()
        skins = images.case0 + images.case1
        while True:
            try:
                self.connected = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print "Connecting to",HOST,PORT
                self.connected.connect((HOST, PORT))
                print "connected to",HOST,PORT
                self.player_number = int(self.connected.recv(2))
                print "Player Number:",self.player_number
                self.skin = SKINS[selected_skin]

                self.name = NAME
                playerinformation = "{<GLOBALS>};client_globals.player" + str(self.player_number) + "_position_y = 300;"\
                                    + "client_globals.player" + str(self.player_number) + "_position_x = 400;"\
                                    + "client_globals.player" + str(self.player_number) + "_name = '" + self.name + "';"\
                                    + "client_globals.player" + str(self.player_number) + "_color = (255,255,255);"\
                                    + "client_globals.player" + str(self.player_number) + "_angle = 0;"\
                                    + "client_globals.player" + str(self.player_number) + "_hp = 1;"\
                                    + "client_globals.player" + str(self.player_number) + "_hpmultiplier = 1;"\
                                    + "client_globals.player" + str(self.player_number) + "_kills = 0;"\
                                    + "client_globals.player" + str(self.player_number) + "_money = 0;"\
                                    + "client_globals.player" + str(self.player_number) + "_skin = " + str(self.skin) + ";"

                playercommands = "self.players.add(player(self.screen," + str(self.player_number)\
                                 + ",(client_globals.player" + str(self.player_number) + "_position_x,"\
                                 + "client_globals.player" + str(self.player_number) + "_position_y)));{<ENDGLOBALS>};"

                print "Sending player information..."
                #print playerinformation+playercommands
                self.connected.sendall(playerinformation + playercommands)
                self.connected.setblocking(0)
                break
            except:
                print "Failed to connect. Trying again..."
        client_globals.offsety = 0
        client_globals.offsetx = 0
        self.offsetx = 0 
        self.offsety = 0
        self.image = skins[self.skin]
        
        self.players = pygame.sprite.Group()

        self.shot_sprites = pygame.sprite.Group()

        self.asteroid_sprites = pygame.sprite.Group()
        
        self.parentgroup = parentgroup
        
        self.recieved_data = ""

        self.send_data = ""
        
        self.posw = 400
        self.posh = 300
        self.spawntime = 60
        self.shotspeed_max = 60
        self.shotspeed = 60
        self.clocktime = 0
        self.rect = pygame.rect.Rect(self.posw,self.posh,40,40)

        self.font = pygame.font.SysFont(None,int(60*client_globals.global_multiplier))
        self.font2 = pygame.font.SysFont(None,int(20*client_globals.global_multiplier))
        self.font3 = pygame.font.SysFont(None,int(15*client_globals.global_multiplier))
        self.killedasteroids = 0
        self.requiredasteroids = 0
        self.kills = 0
        self.speed = 0.5

        self.hp = 1

        self.hpmultiplier = 1
        
        self.money = 0

        self.wave = 1
        self.damage = 1
        self.clickspeed = 20

        self.music = sounds.battle_song.play()
        self.music.stop()

        self.prices = [250,500,1000,500]
        self.max_upgrades = [6,6,10,3]
        self.current_upgrades = [0,0,0,0]

        self.dead = False

        self.won = False
    def update(self):
        self.rect = pygame.rect.Rect(self.posw-15,self.posh-15,30,30)
        #self.rect = pygame.draw.rect(self.screen,(255,255,255),(self.posw-15,self.posh-15,30,30))
        #pygame.draw.rect(self.screen,(255,255,255),(self.posw-800+client_globals.offsetx,self.posh+client_globals.offsety ,800,600))
        #pygame.draw.rect(self.screen,(255,0,0),(self.posw+client_globals.offsetx,self.posh-600+client_globals.offsety ,800,600))
        #pygame.draw.rect(self.screen,(0,255,0),(self.posw-800+client_globals.offsetx,self.posh-600+client_globals.offsety ,800,600))
        #pygame.draw.rect(self.screen,(0,0,255),(self.posw+client_globals.offsetx,self.posh+client_globals.offsety ,800,600))

        self.screen.blit(images.background,(self.posw+client_globals.offsetx*1.25,self.posw+client_globals.offsety*1.25))
        self.screen.blit(images.background,(self.posw+client_globals.offsetx*1.25-800,self.posw+client_globals.offsety*1.25))
        self.screen.blit(images.background,(self.posw+client_globals.offsetx*1.25,self.posw+client_globals.offsety*1.25-600))
        self.screen.blit(images.background,(self.posw+client_globals.offsetx*1.25-800,self.posw+client_globals.offsety*1.25-600))

        x = self.posw-client_globals.offsetx
        y = self.posh-client_globals.offsety
        #print x,y
        hp = self.hp
        kills = self.killedasteroids
        try:
            self.recieved_data = self.connected.recv(2048)
            self.process()
        except:
            None


        #self.rect = pygame.draw.rect(self.screen,(255,255,255),(self.posw,self.posh,10,10))
        pos = pygame.mouse.get_pos()
        screen_size = self.screen.get_size()
        key = pygame.key.get_pressed()
        if key[pygame.K_TAB]:
            self.screen.blit(images.leader,(100,100))
            text = self.font2.render(self.name + " (Player" + str(self.player_number) + ") Kills: " + str(self.kills) + " | Money: " + str(self.money),255,(255,255,255))
            player_pos = 130
                
            self.screen.blit(text,(110,player_pos))
            for i in self.players:
                player_pos += 20
                player_kills = i.kills
                player_money = i.money
                text = self.font2.render(i.name + " (Player" + str(i.player_number) + ") Kills: " + str(player_kills) + " | Money: " + str(player_money),255,(200,200,200))
                self.screen.blit(text,(110,player_pos))
        
        if self.clocktime <= 0:
            if key[pygame.K_a]:
                client_globals.offsetx += self.speed
                self.offsetx += self.speed
            elif key[pygame.K_d]:
                client_globals.offsetx -= self.speed
                self.offsetx -= self.speed
            if key[pygame.K_w]:
                client_globals.offsety += self.speed
                self.offsety += self.speed
            elif key[pygame.K_s]:
                client_globals.offsety -= self.speed
                self.offsety -= self.speed

                
            #if self.posw > screen_size[0]:
            #    self.posw = 0
            #if self.posw < 0:
            #    self.posw = screen_size[0]
            #if self.posh > screen_size[1]:
            #    self.posh = 0
            #if self.posh < 0:
            #    self.posh = screen_size[1]
            
            #pygame.display.update()
            mouse = pygame.mouse.get_pressed()[0]
            self.shotspeed -= 1
            if mouse and self.shotspeed < 0:
                self.shotspeed = self.shotspeed_max
                self.send_data += "self.shot_sprites.add(shot(" + str(self.player_number) + ",self.screen,(" + str(self.posw-self.offsetx) + "," + str(self.posh-self.offsety) + "),(" + str(pos[0]-self.offsetx) + "," + str(pos[1]-self.offsety) + ")));"
            if self.music.get_busy() == 0:
                self.music = sounds.battle_song.play()
            elif self.music.get_sound() == sounds.paused_song:
                self.music.fadeout(1000)
            if self.dead:
                self.posw = -1000
                self.posh = -1000
                client_globals.offsetx = 1400
                client_globals.offsety = 1300
                self.offsety = 1400
                self.offsetx = 1300
                self.shotspeed = self.shotspeed_max
            

        else:
            if self.dead:
                self.posw = 400
                self.posh = 300
                client_globals.offsetx = 0
                client_globals.offsety = 0
                self.offsety = 0
                self.offsetx = 0
                self.money = int(self.money / 2)
                for i in self.current_upgrades:
                    i = int(i / 2)
                self.dead = False
            if self.music.get_busy() == 0:
                self.asteroid_sprites.empty()
                self.music = sounds.paused_song.play()
            elif self.music.get_sound() == sounds.battle_song:
                self.asteroid_sprites.empty()
                self.music.fadeout(1000)
            self.hp = self.hpmultiplier

        healthbar_red = pygame.draw.rect(self.screen,(200,0,0),(self.posw-20, self.posh+20,50,10))
        healthbar_green = pygame.draw.rect(self.screen,(0,200,0),(self.posw-20, self.posh+20,self.hp * 50 / self.hpmultiplier,10))
        name_display = self.font3.render(self.name,255,(255,255,255))
        self.screen.blit(name_display,(self.posw-20,self.posh+20))
        if self.clocktime <= 0:
            angle = 360-math.atan2(pos[1]-self.posh,pos[0]-self.posw)*180/math.pi
        else:
            angle = 0  
        
        rotimage = pygame.transform.rotate(self.image,angle)
        rect = rotimage.get_rect(center=(self.posw,self.posh))
        self.screen.blit(rotimage,rect) #I need space_ship to rotate towards my cursor

        
        #SPAWN ASTEROIDS
        self.spawntime -= 1
        if self.spawntime < 0:
            spawnside = random.randint(0,3)
            if spawnside == 0:
                "LEFT"
                aposw = -100
                aposh = random.randint(0,600) * 2

                speedw = random.randint(2,10)
                speedh = random.randint(-10,10)
                
            if spawnside == 1:
                "RIGHT"
                aposw = 800 * 2
                aposh = random.randint(0,600) * 2
                
                speedw = -random.randint(2,10)
                speedh = random.randint(-10,10)
            if spawnside == 2:
                "TOP"
                aposw = random.randint(0,800) * 2
                aposh = -100
                
                speedw = random.randint(-10,10)
                speedh = random.randint(2,10)
            if spawnside == 3:
                "BOTTOM"
                aposw = random.randint(0,800) * 2
                aposh = 600 * 2
                
                speedw = random.randint(-10,10)
                speedh = -random.randint(2,10)
            if self.clocktime <= 0:
                atype = random.randint(0,100)
                self.send_data += "self.asteroid_sprites.add(asteroid(self.screen,(" + str(aposw) + "," + str(aposh) + "),(" + str(speedw) + "," + str(speedh) + "),"+str(atype) + "));"
                divider = self.wave / 2
                if divider == 0:
                    divider = 1
                self.spawntime = 180 / divider
            else:
                self.spawntime = 0

        #print "Global position x",self.posw-client_globals.offsetx,"Global position y",self.posh-client_globals.offsety
        position_commands = "client_globals.player" + str(self.player_number)+ "_position_y = " + str(float(self.posh-self.offsety)) + ";"\
                            + "client_globals.player" + str(self.player_number)+ "_position_x = " + str(float(self.posw-self.offsetx)) + ";"
        self.send_data += "client_globals.player" + str(self.player_number)+ "_angle = " + str(angle) + ";"
        if self.posw-client_globals.offsetx != x or self.posh-client_globals.offsety != y:
            self.send_data += position_commands


        if self.clocktime > 0:
            clock_text = self.font.render("Time until next wave: " +str(self.clocktime),255,(255,255,255))
            self.screen.blit(images.shop,(100,100))

            mousepos = pygame.mouse.get_pos()
            mouserect = pygame.rect.Rect(mousepos[0],mousepos[1],1,1)
            self.screen.blit(images.buy,(660*client_globals.global_multiplier,130*client_globals.global_multiplier))
            self.screen.blit(images.buy,(370*client_globals.global_multiplier,130*client_globals.global_multiplier))
            self.screen.blit(images.buy,(370*client_globals.global_multiplier,150*client_globals.global_multiplier))
            self.screen.blit(images.buy,(660*client_globals.global_multiplier,150*client_globals.global_multiplier))
            
            rect1 = pygame.rect.Rect(370*client_globals.global_multiplier,130*client_globals.global_multiplier,30*client_globals.global_multiplier,20*client_globals.global_multiplier)
            rect2 = pygame.rect.Rect(660*client_globals.global_multiplier,130*client_globals.global_multiplier,30*client_globals.global_multiplier,20*client_globals.global_multiplier)
            rect3 = pygame.rect.Rect(370*client_globals.global_multiplier,150*client_globals.global_multiplier,30*client_globals.global_multiplier,20*client_globals.global_multiplier)
            rect4 = pygame.rect.Rect(660*client_globals.global_multiplier,150*client_globals.global_multiplier,30*client_globals.global_multiplier,20*client_globals.global_multiplier)
            
            buy_movement = self.font2.render("Money: "+str(self.money),255,(255,255,255))
            self.screen.blit(buy_movement,(620*client_globals.global_multiplier,110*client_globals.global_multiplier))

            buy_movement = self.font2.render(str(self.current_upgrades[0]) + "/" + str(self.max_upgrades[0]) + " Movement Speed Upgrade ($" +str(self.prices[0]) + ")",255,(255,255,255))
            buy_firerate = self.font2.render(str(self.current_upgrades[1]) + "/" + str(self.max_upgrades[1]) + " Fire Rate Upgrade ($" +str(self.prices[1]) + ")",255,(255,255,255))
            buy_hp = self.font2.render(str(self.current_upgrades[2]) + "/" + str(self.max_upgrades[2]) +" Max Health Upgrade ($" +str(self.prices[2]) + ")",255,(255,255,255))
            buy_damage = self.font2.render(str(self.current_upgrades[3]) + "/" + str(self.max_upgrades[3]) +" Damage Upgrade ($" +str(self.prices[3]) + ")",255,(255,255,255))
            self.screen.blit(buy_movement,(110*client_globals.global_multiplier,130*client_globals.global_multiplier))
            self.screen.blit(buy_firerate,(410*client_globals.global_multiplier,130*client_globals.global_multiplier))
            self.screen.blit(buy_hp,(110*client_globals.global_multiplier,150*client_globals.global_multiplier))
            self.screen.blit(buy_damage,(410*client_globals.global_multiplier,150*client_globals.global_multiplier))
            self.screen.blit(clock_text,(150*client_globals.global_multiplier,10*client_globals.global_multiplier))

            self.clickspeed -= 1
            if self.clickspeed <= 0 and pygame.mouse.get_pressed()[0]:
                self.clickspeed = 20
                if mouserect.colliderect(rect1):
                    if self.money >= self.prices[0] and self.current_upgrades[0] < self.max_upgrades[0]:
                        print "Purchased."
                        self.speed += 0.25
                        self.money -= self.prices[0]
                        self.prices[0] = int(self.prices[0] * 1.25)
                        self.current_upgrades[0] += 1
                        sounds.purchased.play()
                    else: sounds.click.play()
                elif mouserect.colliderect(rect2):
                    if self.money >= self.prices[1] and self.current_upgrades[1] < self.max_upgrades[1]:
                        print "Purchased."
                        self.money -= self.prices[1]
                        self.prices[1] = int(self.prices[1] * 1.35)
                        self.current_upgrades[1] += 1
                        self.shotspeed_max -= 8
                        sounds.purchased.play()
                    else: sounds.click.play()
                elif mouserect.colliderect(rect3):
                    if self.money >= self.prices[2] and self.current_upgrades[2] < self.max_upgrades[2]:
                        print "Purchased."
                        self.money -= self.prices[2]
                        self.current_upgrades[2] += 1
                        self.prices[2] = int(self.prices[2] * 1.25) 
                        self.hpmultiplier += 1
                        sounds.purchased.play()
                        self.send_data += "client_globals.player" + str(self.player_number) + "_hp = " + str(self.hp) + ";"
                        self.send_data += "client_globals.player" + str(self.player_number) + "_hpmultiplier = " + str(self.hpmultiplier) + ";"
                    else: sounds.click.play()

                elif mouserect.colliderect(rect4):
                    if self.money >= self.prices[3] and self.current_upgrades[3] < self.max_upgrades[3]:
                        print "Purchased."
                        self.money -= self.prices[3]
                        self.current_upgrades[3] += 1
                        self.prices[3] = int(self.prices[3] * 5) 
                        self.damage += 1
                        sounds.purchased.play()
                    else: sounds.click.play()
                        
        else:
            clock_text = self.font.render("Asteriods Killed: " +str(self.killedasteroids) + " / " + str(self.requiredasteroids),255,(255,255,255))
            self.screen.blit(clock_text,(130,10))
            

        self.players.update()
        self.shot_sprites.update()
        self.asteroid_sprites.update()
        collision_ = pygame.sprite.groupcollide(self.shot_sprites,self.asteroid_sprites,0,0)   
        collision = pygame.sprite.groupcollide(self.asteroid_sprites,self.shot_sprites,0,1)
        collision3 = pygame.sprite.groupcollide(self.asteroid_sprites,self.players,1,0)
        if collision:
            for asteroid in collision:
                for shot in collision_:
                    asteroid.hp -= self.damage
                    if asteroid.hp <= 0:
                        if shot.owner == self.player_number:
                            asteroid.killedby = self.player_number
                            self.kills += 1
                            self.send_data += "client_globals.player" + str(self.player_number) + "_kills = " + str(self.kills) + ";"
        for i in self.asteroid_sprites:
            if i.justDied == 1:
                self.killedasteroids += 1
                self.send_data += "self.killedasteroids = " + str(self.killedasteroids) + ";"
                self.send_data += "self.money += " + str(10 * i.tier) + ";"
                self.money += 10 * i.tier
                i.justDied = -1
        collision2 = pygame.sprite.groupcollide(self.asteroid_sprites,self.parentgroup,1,0)
        if collision2:
            self.hp -= 1
            if self.hp <= 0:
                self.dead = True
                #self.connected.sendall("<{DROP" + str(self.player_number) + "}>;")
                #self.kill()
        self.screen.blit(images.mousec, (pos[0] - 12,pos[1] - 12))
        if hp != self.hp:
            self.send_data += "client_globals.player" + str(self.player_number) + "_hp = " + str(self.hp) + ";"
            self.send_data += "client_globals.player" + str(self.player_number) + "_hpmultiplier = " + str(self.hpmultiplier) + ";"

        if kills != self.kills:
            self.send_data += ""
            
        try:
            self.connected.sendall(self.send_data)
            self.send_data = ""
        except:
            pass

                
    def remove_player(self,playernumber):
        for i in self.players:
            if i.player_number == playernumber:
                i.kill()
    def process(self):
        new_data = []
        data = self.recieved_data
        data = data.split(";")
        data.pop()
        for i in data:
            if i not in new_data:
                if " " in i:
                    i = i.replace(" ","")
                new_data.append(i)
        
        for i in new_data:
            try:
                #print "Executing",i
                if "self.shot_sprites.add(shot(" + str(self.player_number) in i:
                    pos = pygame.mouse.get_pos()
                    self.shot_sprites.add(shot(self.player_number,self.screen,(self.posw-self.offsetx,self.posh-self.offsety),(pos[0]-self.offsetx,pos[1]-self.offsety)))
                elif str("player" + str(self.player_number)) not in i:
                    if "money" in i:
                        self.send_data += "client_globals.player" + str(self.player_number) + "_money = " + str(self.money) + ";"
                    exec(i)
            except:
                "Invalid command",i
