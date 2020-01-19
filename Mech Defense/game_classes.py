import pygame
pygame.font.init()
import network_classes
import ast
import random
import math
import images
from funct import *
import funct
class enemy(pygame.sprite.Sprite):
    def __init__(self,display,(x,y,ID,hp,damage,speed),(enemyclass,serverplayers,localplayer)):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.localplayer = localplayer
        self.serverplayers = serverplayers
        self.enemyclass = enemyclass
        self.hp = hp
        self.uniqueID = ID
        self.damage = damage
        self.speed = speed
        self.x = x
        self.y = y
        self.globalx = 0
        self.globaly = 0
        self.image = images.e_beetle
        self.enemypositions = []
    def closestPlayerTrajectory(self):
        self.enemypositions = []
        for i in self.serverplayers:
            self.enemypositions.append((i.x,i.y))
        self.enemypositions.append((self.localplayer.x + self.localplayer.global_x,self.localplayer.y + self.localplayer.global_y))
        distances = []
        for i in self.enemypositions:
            dx = self.x - i[0]
            dy = self.y - i[1]
            self.dist = max(1,math.hypot(dx,dy))
            distances.append(self.dist)
        
        target = min(float(s) for s in distances)
        seek_target = self.enemypositions[distances.index(target)]

        self.gotox = seek_target[0]
        self.gotoy = seek_target[1]
        self.dx = seek_target[0]-float(self.x)
        self.dy = seek_target[1]-float(self.y)
        
        self.slope = (self.dy/max(1,self.dx))
        self.gotox += self.gotox * self.slope
        self.gotoy += self.gotoy * self.slope
        dist = max(1, math.hypot(self.dx, self.dy))
        vx = self.speed * (self.dx / dist)
        vy = self.speed * (self.dy / dist)
        return vx,vy
    def update(self):
        ####DEBUGGGGGG
        self.kill()
        vx,vy = self.closestPlayerTrajectory()
        self.x += vx
        self.y += vy
        angle = 360-math.atan2(self.dy,self.dx)*180/math.pi
        r = pygame.transform.rotate(self.image,angle)
        rect = r.get_rect(center=(self.x-self.localplayer.global_x,self.y-self.localplayer.global_y))
        self.localplayer.client.send_updates("{A}(" + str(self.uniqueID) + "," + str(self.x) + "," + str(self.y) + ")|")
        self.display.blit(r,rect)

class bullet(pygame.sprite.Sprite):
    def __init__(self,display,(pos1,pos2),(endpos1,endpos2),speed,damage,tracer):
        pygame.sprite.Sprite.__init__(self)
        self.screen = display
        self.ogposx,self.ogposy = (pos1,pos2)
        self.ogendx,self.ogendy = (endpos1,endpos2)
        mousepos = (endpos1,endpos2)
        self.gotox = float(mousepos[0])
        self.gotoy = float(mousepos[1])
        self.dx = mousepos[0]-float(pos1)
        self.dy = mousepos[1]-float(pos2)
        
        self.slope = (self.dy/max(1,self.dx))
        self.gotox += self.gotox * self.slope
        self.gotoy += self.gotoy * self.slope

        self.dist = max(1,math.hypot(self.dx,self.dy))
        
        self.speed = speed
        self.damage = damage
        self.posx, self.posy = (pos1,pos2)
        self.decay_time = 60
        self.rect = pygame.rect.Rect(0,0,0,0)
        self.image = pygame.surface.Surface((2,2))
        if tracer:
            self.image.fill((255,75,46))
        else:
            self.image.fill((255,200,100))
        self.globalx,self.globaly = (0,0)
        self.animc = 0
        self.frame = 0
    def update(self):
        self.decay_time -= 1
        self.rect = pygame.rect.Rect(self.posx,self.posy,2,2)
        if self.decay_time < 0:
            self.animc -= 1
            if self.animc < 0 and self.frame < 5:
                self.animc = 5
                self.frame += 1
                self.image = images.bullet_impact[self.frame]
            else:
                self.image = images.bullet_impact[5]
            self.screen.blit(self.image,(self.stoppedx,self.stoppedy))
        else:
            mousepos = (self.ogendx,self.ogendy)
            self.gotox = float(mousepos[0])
            self.gotoy = float(mousepos[1])
            self.dx = mousepos[0]-float(self.ogposx)
            self.dy = mousepos[1]-float(self.ogposy)
            
            self.slope = (self.dy/max(1,self.dx))
            self.gotox += self.gotox * self.slope
            self.gotoy += self.gotoy * self.slope
            
            self.dist = max(1,math.hypot(self.dx,self.dy))
            self.vx = self.speed * (self.dx / self.dist)
            self.vy = self.speed * (self.dy / self.dist)
            self.posx += self.vx
            self.posy += self.vy
            self.stoppedx,self.stoppedy = (self.posx,self.posy)
            self.screen.blit(self.image,(self.posx,self.posy))

class serverPlayer(pygame.sprite.Sprite):
    def __init__(self,display,bullet_class,ID):
        pygame.sprite.Sprite.__init__(self)
        self.bulletClass = bullet_class
        self.x = 0
        self.y = 0
        self.global_x = 0
        self.global_y = 0
        self.display = display
        self.image = pygame.surface.Surface((20,20))
        self.image.fill((255,255,255))
        self.uniqueID = ID
        self.name = ""
        self.nametext = pygame.font.SysFont(None,18)
        self.selected_skin = -1
        self.angle = 0
        self.tracer = 5
        self.ct = 0
        self.tracer2 = 5
        self.ct2 = 0
        self.shot_animation_speed = 5
        self.animframe = 6
        self.shotanim = 3
        self.animframe2 = 6
        self.shotanim2 = 3
        self.shooting = False
        self.shooting2 = False
        self.gun_type1 = 0
        self.gun_type2 = 0
        self.blank = pygame.surface.Surface((0,0))
        self.blank.set_alpha(0)
        
    def update(self):
        name = self.nametext.render(self.name,255,(255,255,255))
        mecharms = images.mech_arms.copy()
        mecharms.blit(self.playshotanimation(0),(0,0))
        mecharms.blit(self.playshotanimation(1),(0,0))
        rotbody = pygame.transform.rotate(self.image,self.angle)
        rotarms = pygame.transform.rotate(mecharms,self.angle)
        rect = rotbody.get_rect(center=(self.x-self.global_x,self.y-self.global_y))
        rect2 = rotarms.get_rect(center=(self.x-self.global_x,self.y-self.global_y))
        self.display.blit(rotbody,rect)
        self.display.blit(rotarms,rect2)
        self.display.blit(name,(self.x-self.global_x-15,self.y-self.global_y-22))
    def playshotanimation(self,gunnum):
        if gunnum == 0:
            self.shotanim -= 1
            if self.shotanim < 0:
                self.shotanim = self.shot_animation_speed
                self.animframe += 1
                
            if self.shooting:
                if self.animframe > 0:
                    self.animframe = 0
            else:
                if self.animframe > 6:
                    self.shotanim = self.shot_animation_speed
                    self.animframe = 6
                    
            if self.animframe != 6:
                if self.gun_type1 in [3,4,5,11,12,13,14]:
                    return images.gun1l_anim[self.animframe]
                elif self.gun_type1 in [0,1,2]:
                    return images.gun0l_anim[self.animframe]
                elif self.gun_type1 in [6,7,8,9,10]:
                    return images.gun2l_anim[self.animframe]
            else:
                return self.blank
        if gunnum == 1:
            self.shotanim2 -= 1
            if self.shotanim2 < 0:
                self.shotanim2 = self.shot_animation_speed
                self.animframe2 += 1
            if self.shooting2:
                if self.animframe2 > 0:
                    self.animframe2 = 0
            else:
                if self.animframe2 > 6:
                    self.shotanim2 = self.shot_animation_speed
                    self.animframe2 = 6
                    
            if self.animframe2 != 6:
                if self.gun_type2 in [3,4,5,11,12,13,14]:
                    return images.gun1r_anim[self.animframe2]
                elif self.gun_type2 in [0,1,2]:
                    return images.gun0r_anim[self.animframe2]
                elif self.gun_type2 in [6,7,8,9,10]:
                    return images.gun2r_anim[self.animframe2]
            else:
                return self.blank
    def updateMe(self,update):
        self.angle = update[6]
        self.x = update[0]
        self.y = update[1]
        self.name = update[2]
        self.gun_type1 = update[7][0]
        self.gun_type2 = update[7][1]
        if update[3] != None:
            self.ct += 1
            if self.ct >= self.tracer:
                self.ct = 0
                tracer = True
            else:
                tracer = False
            self.shooting = True
            bi = update[3]
            sangle = -math.radians(self.angle-180)
            shoot_pos1 = rotatePoint((self.x-self.global_x,self.y-self.global_y),(self.x-self.global_x,self.y-self.global_y+18),sangle)
            
            if bi[4] != 1:
                for i in range(0,bi[4]):
                    self.bulletClass.add(bullet(self.display,shoot_pos1,
                                                (bi[1][0]-self.global_x+bi[5][i][0],bi[1][1]-self.global_y+bi[5][i][1]),bi[2],bi[3],tracer))
            else:
                self.bulletClass.add(bullet(self.display,shoot_pos1,
                            (bi[1][0]-self.global_x+bi[5][0][0],bi[1][1]-self.global_y+bi[5][0][1]),bi[2],bi[3],tracer))

            #pygame.draw.rect(self.display,(0,0,150),(bi[1][0]-self.global_x,bi[1][1]-self.global_y,2,2))
        else:
            self.shooting = False
        if update[4] != None:
            self.ct2 += 1
            if self.ct2 >= self.tracer2:
                self.ct2 = 0
                tracer = True
            else:
                tracer = False
            self.shooting2 = True
            bi = update[4]
            sangle = -math.radians(self.angle-180)
            shoot_pos2 = rotatePoint((self.x-self.global_x,self.y-self.global_y),(self.x-self.global_x,self.y-self.global_y-18),sangle)
            if bi[4] != 1:
                for i in range(0,bi[4]):
                    self.bulletClass.add(bullet(self.display,shoot_pos2,
                                                (bi[1][0]-self.global_x+bi[5][i][0],bi[1][1]-self.global_y+bi[5][i][1]),bi[2],bi[3],tracer))
            else:
                self.bulletClass.add(bullet(self.display,shoot_pos2,
                            (bi[1][0]-self.global_x+bi[5][0][0],bi[1][1]-self.global_y+bi[5][0][1]),bi[2],bi[3],tracer))

        else:
            self.shooting2 = False
        if self.selected_skin != update[5]:
            self.selected_skin = update[5]
            self.image = images.skins_default[self.selected_skin ]

class localPlayer(pygame.sprite.Sprite):
    def __init__(self,display):
        pygame.sprite.Sprite.__init__(self)
        self.client = network_classes.Client((funct.savedata[5],funct.savedata[6]))
        self.selected_skin = random.randint(0,4)
        self.image = images.skins_default[self.selected_skin]
        self.display = display
        self.serverPlayers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.bullets = pygame.sprite.Group()
        self.name = ["Poof_wonder","Failed_Abortion","Cateract","Salad_Finger",
                     "Bottom_text","garth?","Markusz","McLovin","TransGardener",
                     "Dinner_Toes","gFUEL","Howitfeelschew5gum","Skype",
                     "Teamspeak>Discord"]
        self.name = self.name[random.randint(0,len(self.name)-1)]
        self.alive = False
        self.locked = True
        self.x = 400
        self.y = 300
        self.global_x = 0
        self.global_y = 0
        self.bullet_speed = 5
        self.bullet_damage = 1
        #(0) .30Cal Rifle (1) .50Cal Rifle (2) .57Cal Rifle (3) .30 LMG (4) .50Cal LMG (5) .57Cal LMG (6) 12 Gauge Quattro (7) 8 Gauge Duo (8) 8 Guage Quattro (9) 4 Guage Duo 
        #(10) 4 Guage Quattro (11) Chaingun (12) Dual Fire Chaingun(13) Minigun (14) Vulcan Cannon (15) RPG-L 65mm (16) RPG-L 105mm (17) RPG-L 155mm (18) 
        self.gun_type1 = 12
        self.gun_type2 = 12
        #Base Gun Firerate
        self.bgf = [45,55,60,
                      18,16,13,
                      90,60,90,60,90,
                      4,5,2,1,
                      60,60,60]
        #Base Gun Number of Shots
        self.bgns = [1,1,1,
                      1,1,1,
                      28,14,28,14,28,
                      1,2,1,1,
                      1,1,1]
        #Base Gun Damage
        self.bgd = [4,7,10,
                    2,3,5,
                    1,2,2,3,3,
                    3,3,4,5,
                    10,12,15]
        #Base Gun Velocity
        self.bgv = [7,9,11,
                      4,6,8,
                      4,6,6,8,8,
                      7,7,6,5,2,3,4]
        #Gun Base Innacuracy
        self.bgi = [3,2,1,
                    5,6,9,
                    50,40,52,42,58,
                    9,11,12,20,4,5,6]
        #Frequency of a tracer shot.
        self.bgtracers = [2,2,2,
                          5,5,5,
                          2,2,2,2,2,
                          6,7,8,9,
                          0,0,0]
        
        self.ct = 0
        self.ct2 = 0
        self.tracer = self.bgtracers[self.gun_type1]
        self.tracer2 = self.bgtracers[self.gun_type2]
        self.gun1 = [self.bgf[self.gun_type1],self.bgns[self.gun_type1],self.bgd[self.gun_type1],self.bgv[self.gun_type1],self.bgi[self.gun_type1]]
        self.gun2 = [self.bgf[self.gun_type2],self.bgns[self.gun_type2],self.bgd[self.gun_type2],self.bgv[self.gun_type2],self.bgi[self.gun_type2]]
        self.cfirerate0 = self.gun1[0]
        self.cfirerate1 = self.gun2[0]

        self.shot_animation_speed = 5
        self.animframe = 6
        self.shotanim = 3
        self.animframe2 =6
        self.shotanim2 = 3
        self.shooting = False
        self.shooting2 = False
        self.blank = pygame.surface.Surface((0,0))
        self.blank.set_alpha(0)
    def display_grid(self):
        #Center
        self.display.blit(images.background,(-self.global_x,-self.global_y))
        #Up
        self.display.blit(images.background,(-self.global_x,-self.global_y-600))
        #Up-Right
        self.display.blit(images.background,(-self.global_x+800,-self.global_y-600))
        #Right
        self.display.blit(images.background,(-self.global_x+800,-self.global_y))
        #Down-Right
        self.display.blit(images.background,(-self.global_x+800,-self.global_y+600))
        #Down
        self.display.blit(images.background,(-self.global_x,-self.global_y+600))
        #Downleft
        self.display.blit(images.background,(-self.global_x-800,-self.global_y+600))
        #Left
        self.display.blit(images.background,(-self.global_x-800,-self.global_y))
        #Up-Left
        self.display.blit(images.background,(-self.global_x-800,-self.global_y-600))

    def playshotanimation(self,gunnum):
        if gunnum == 0:
            self.shotanim -= 1
            if self.shotanim < 0:
                self.shotanim = self.shot_animation_speed
                self.animframe += 1
                
            if self.shooting:
                if self.animframe > 0:
                    self.animframe = 0
            else:
                if self.animframe > 6:
                    self.shotanim = self.shot_animation_speed
                    self.animframe = 6
                    
            if self.animframe != 6:
                if self.gun_type1 in [3,4,5,11,12,13,14]:
                    return images.gun1l_anim[self.animframe]
                elif self.gun_type1 in [0,1,2]:
                    return images.gun0l_anim[self.animframe]
                elif self.gun_type1 in [6,7,8,9,10]:
                    return images.gun2l_anim[self.animframe]
            else:
                return self.blank
        if gunnum == 1:
            self.shotanim2 -= 1
            if self.shotanim2 < 0:
                self.shotanim2 = self.shot_animation_speed
                self.animframe2 += 1
            if self.shooting2:
                if self.animframe2 > 0:
                    self.animframe2 = 0
            else:
                if self.animframe2 > 6:
                    self.shotanim2 = self.shot_animation_speed
                    self.animframe2 = 6
                    
            if self.animframe2 != 6:
                if self.gun_type2 in [3,4,5,11,12,13,14]:
                    return images.gun1r_anim[self.animframe2]
                elif self.gun_type2 in [0,1,2]:
                    return images.gun0r_anim[self.animframe2]
                elif self.gun_type2 in [6,7,8,9,10]:
                    return images.gun2r_anim[self.animframe2]
            else:
                return self.blank
    def update(self):

        self.shot = None
        self.shot2 = None
        if self.client.recvServer():
            self.processData(self.client.getData())

        for i in self.bullets:
            i.globaly,i.globalx = (self.global_y,self.global_x)
        key = pygame.key.get_pressed()
        if self.locked == False:
            if key[pygame.K_w]:
                self.global_y -= 1
            if key[pygame.K_s]:
                self.global_y += 1
            if key[pygame.K_a]:
                self.global_x -= 1
            if key[pygame.K_d]:
                self.global_x += 1

        mousepos = pygame.mouse.get_pos()
        angle = 360-math.atan2(mousepos[1]-self.y,mousepos[0]-self.x)*180/math.pi
        sangle = -math.radians(angle-180)
        mecharms = images.mech_arms.copy()
        
        if  pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            pygame.mouse.set_visible(False)
            pygame.draw.rect(self.display,(0,0,0),(mousepos[0]-1,mousepos[1]-1,5,5))
            pygame.draw.rect(self.display,(255,255,255),(mousepos[0],mousepos[1],3,3))
        else:
            pygame.mouse.set_visible(True)
        if self.locked == False:
            if  pygame.mouse.get_pressed()[0] and self.cfirerate0 <= 0:
                self.ct += 1
                self.shooting = True
                if self.ct >= self.tracer:
                    self.ct = 0
                    tracer = True
                else:
                    tracer = False
                self.cfirerate0 = self.gun1[0]
                shoot_pos1 = rotatePoint((self.x,self.y),(self.x,self.y+18),sangle)
                inaccuracy = []
                
                for i in range(0,self.gun1[1]):
                    inaccuracy.append((random.randint(-self.gun2[4],self.gun2[4]),random.randint(-self.gun2[4],self.gun2[4])))
                self.shot = (shoot_pos1,(mousepos[0]+self.global_x,mousepos[1]+self.global_y),self.gun1[3],self.gun1[2],self.gun1[1],inaccuracy)

                for i in range(0,self.gun1[1]):
                    self.bullets.add(bullet(self.display,(shoot_pos1),(mousepos[0]+inaccuracy[i][0],mousepos[1]+inaccuracy[i][1]),self.gun1[3],self.gun1[2],tracer))
                    
                #self.bullets.add(bullet(self.display,(shoot_pos1),(mousepos[0],mousepos[1]),self.bullet_speed,self.bullet_damage))
            else:
                self.shooting = False
            if pygame.mouse.get_pressed()[2] and self.cfirerate1 <= 0:
                self.ct2 += 1
                self.shooting2 = True
                if self.ct2 >= self.tracer2:
                    self.ct2 = 0
                    tracer = True
                else:
                    tracer = False
                self.cfirerate1 = self.gun2[0]
                shoot_pos2 = rotatePoint((self.x,self.y),(self.x,self.y-18),sangle)
                inaccuracy = []
                for i in range(0,self.gun2[1]):
                    inaccuracy.append((random.randint(-self.gun2[4],self.gun2[4]),random.randint(-self.gun2[4],self.gun2[4])))
                self.shot2 = (shoot_pos2,(mousepos[0]+self.global_x,mousepos[1]+self.global_y),self.gun2[3],self.gun2[2],self.gun2[1],inaccuracy)

                for i in range(0,self.gun2[1]):
                    self.bullets.add(bullet(self.display,(shoot_pos2),(mousepos[0]+inaccuracy[i][0],mousepos[1]+inaccuracy[i][1]),self.gun2[3],self.gun2[2],tracer))
            else:
                self.shooting2 = False
        mecharms.blit(self.playshotanimation(0),(0,0))
        mecharms.blit(self.playshotanimation(1),(0,0))
        rotbody = pygame.transform.rotate(self.image,angle)
        rotarms = pygame.transform.rotate(mecharms,angle)
        rect = rotbody.get_rect(center=(self.x,self.y))
        rect2 = rotarms.get_rect(center=(self.x,self.y))
        self.display_grid()
        self.bullets.update()
        self.serverPlayers.update()
        if self.locked == False:
            self.display.blit(rotbody,rect)
            self.display.blit(rotarms,rect2)
        else:
            fontBox(self.display,pygame.font.SysFont(None,96),"Waiting for next wave...",(400,500),(100,100,100))
        self.enemies.update()
        self.cfirerate0 -= 1
        self.cfirerate1 -= 1


        info = "{P"+str(self.client.uniqueID) + "}=[" +\
                str(self.x + self.global_x) + "," + str(self.y + self.global_y) + ",'" + self.name + "'," + str(self.shot) +"," +str(self.shot2)+ ","+str(self.selected_skin) + ","\
                + str(angle) + "," + str((self.gun_type1,self.gun_type2)) + "]|"
        self.client.send_updates(info)
        
    def processData(self,data):
        for i in data:
            #Player update.
            if i.startswith("F") and self.alive == False:

                self.alive = True
                self.enemies.empty()
            elif i.startswith("T") and self.alive == False:
                self.locked = True
            elif i.startswith("T") and self.alive == True:
                self.locked = False
            elif i.startswith("F") and self.alive == True:
                self.enemies.empty()
            if i.startswith("{SE}"):
                i = i[4:]
                dataf = ast.literal_eval(i)
                self.enemies.add(enemy(self.display,(dataf[0],dataf[1],dataf[2],dataf[3],dataf[4],dataf[5]),(self.enemies,self.serverPlayers,self)))
            if i.startswith("{P"):
                i = i[2:]
                c = i.split("=")
                playerID = int(c[0].replace("}",""))
                dataf = ast.literal_eval(c[1])
                for p in self.serverPlayers:
                    if playerID == p.uniqueID:
                        p.updateMe(dataf)
                        p.global_x, p.global_y = (self.global_x,self.global_y)
            if i.startswith("{NPU}="):
                i = i[6:]
                if len(i) != 0:
                    dataf = ast.literal_eval(i)
                for opuid in dataf:
                    if type(opuid) == int:
                        add_player = True
                        for opu in self.serverPlayers:
                            #print type(opuid),type(self.uniqueID)
                            if opuid == self.client.uniqueID:
                                print "is Local Player."
                                add_player = False
                            if opuid == opu.uniqueID:
                                print "Player Exists already!"
                                add_player = False                    
                                print "Defining player."
                        if add_player:
                            if opuid != self.client.uniqueID:
                                    print "Creating player",opuid
                                    self.serverPlayers.add(serverPlayer(self.display,self.bullets,opuid))

                    else:
                        for opu in self.serverPlayers:

                            if opu.uniqueID == int(opuid):
                                opu.kill()
                            
                        
            
                    
                    
                
