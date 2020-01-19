import pygame
import os
from funct import *

splash = [img("./data/img/menu_splash/splash1.png"),
          img("./data/img/menu_splash/python.png"),
          img("./data/img/menu_splash/pygame.png"),
          img("./data/img/menu_splash/main_menu.png")]
bullet_impact = img(os.listdir('./data/img/guns/projectiles/bullet_hit'),'./data/img/guns/projectiles/bullet_hit/')
wheel = img(os.listdir('data/img/menu_splash/loadingwheel'),'data/img/menu_splash/loadingwheel/')
background = img("./data/img/background/background.jpg")
mech_arms = img("./data/img/players/mech_arms.png")
e_beetle = img("./data/img/enemies/default/beetle.png")
skins_default = [img("./data/img/players/default/mech_Default.png"),
                 img("./data/img/players/default/mech_waldo.png"),
                 img("./data/img/players/default/mech_baseball.png"),
                 img("./data/img/players/default/mech_construction.png"),
                 img("./data/img/players/default/mech_circuit.png"),
                 img("./data/img/players/default/mech_patriotic.png"),
                 img("./data/img/players/default/mech_redboi.png"),
                 img("./data/img/players/default/mech_ghost.png")]
gun2r_anim = [img("./data/img/guns/gun_2/anim00.png"),
              img("./data/img/guns/gun_2/anim01.png"),
              img("./data/img/guns/gun_2/anim02.png"),
              img("./data/img/guns/gun_2/anim03.png"),
              img("./data/img/guns/gun_2/anim04.png"),
              img("./data/img/guns/gun_2/anim05.png"),
              img("./data/img/guns/gun_2/anim06.png")]
gun2l_anim = [img("./data/img/guns/gun_2/anim10.png"),
              img("./data/img/guns/gun_2/anim11.png"),
              img("./data/img/guns/gun_2/anim12.png"),
              img("./data/img/guns/gun_2/anim13.png"),
              img("./data/img/guns/gun_2/anim14.png"),
              img("./data/img/guns/gun_2/anim15.png"),
              img("./data/img/guns/gun_2/anim16.png")]
gun1r_anim = [img("./data/img/guns/gun_1/anim00.png"),
              img("./data/img/guns/gun_1/anim01.png"),
              img("./data/img/guns/gun_1/anim02.png"),
              img("./data/img/guns/gun_1/anim03.png"),
              img("./data/img/guns/gun_1/anim04.png"),
              img("./data/img/guns/gun_1/anim05.png"),
              img("./data/img/guns/gun_1/anim06.png")]
gun1l_anim = [img("./data/img/guns/gun_1/anim10.png"),
              img("./data/img/guns/gun_1/anim11.png"),
              img("./data/img/guns/gun_1/anim12.png"),
              img("./data/img/guns/gun_1/anim13.png"),
              img("./data/img/guns/gun_1/anim14.png"),
              img("./data/img/guns/gun_1/anim15.png"),
              img("./data/img/guns/gun_1/anim16.png")]
gun0r_anim = [img("./data/img/guns/gun_0/anim00.png"),
              img("./data/img/guns/gun_0/anim01.png"),
              img("./data/img/guns/gun_0/anim02.png"),
              img("./data/img/guns/gun_0/anim03.png"),
              img("./data/img/guns/gun_0/anim04.png"),
              img("./data/img/guns/gun_0/anim05.png"),
              img("./data/img/guns/gun_0/anim06.png")]
gun0l_anim = [img("./data/img/guns/gun_0/anim10.png"),
              img("./data/img/guns/gun_0/anim11.png"),
              img("./data/img/guns/gun_0/anim12.png"),
              img("./data/img/guns/gun_0/anim13.png"),
              img("./data/img/guns/gun_0/anim14.png"),
              img("./data/img/guns/gun_0/anim15.png"),
              img("./data/img/guns/gun_0/anim16.png")]
