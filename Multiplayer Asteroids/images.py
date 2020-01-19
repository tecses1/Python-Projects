import pygame
import images
scale_factor = 0
def loadimg(path,scale=1):
    scale = images.scale_factor
    image = pygame.image.load(path)
    image_size = image.get_size()
    print image_size[0] * scale,image_size[1] * scale
    image_size = (int(float(image_size[0]) * scale),
                  int(float(image_size[1]) * scale))
    image = pygame.transform.scale(image,image_size)
    return image
    
def load_images(scale):
    images.scale_factor = scale
    images.mousec = loadimg("images/1024px-Crosshairs_Red.svg.png")

    images.asteroid1 = loadimg("images/asteroid1.png")
    images.asteroid2 = loadimg("images/asteroid2.png")
    images.asteroid3 = loadimg("images/asteroid3.png")
    images.asteroid4 = loadimg("images/asteroid4.png")
    images.asteroid5 = loadimg("images/asteroid5.png")

    images.background = loadimg("images/background.png")
    images.won = loadimg("images/win.png")
    images.explosion_anim = [loadimg("images/explosion/frame0.gif"),
                      loadimg("images/explosion/frame1.gif"),
                      loadimg("images/explosion/frame2.gif"),
                      loadimg("images/explosion/frame3.gif"),
                      loadimg("images/explosion/frame4.gif"),
                      loadimg("images/explosion/frame5.gif"),
                      loadimg("images/explosion/frame6.gif"),
                      loadimg("images/explosion/frame7.gif"),
                      loadimg("images/explosion/frame8.gif"),
                      loadimg("images/explosion/frame9.gif"),
                      loadimg("images/explosion/frame10.gif"),
                      loadimg("images/explosion/frame11.gif"),
                      loadimg("images/explosion/frame12.gif"),
                      loadimg("images/explosion/frame13.gif"),
                      loadimg("images/explosion/frame14.gif"),
                      loadimg("images/explosion/frame15.gif"),
                      loadimg("images/explosion/frame16.gif")]

    images.reel = loadimg("images/cases/openimgs/reel.png")
    images.rarities = [loadimg("images/cases/openimgs/common.png"),
                loadimg("images/cases/openimgs/uncommon.png"),
                loadimg("images/cases/openimgs/rare.png"),
                loadimg("images/cases/openimgs/covert.png"),
                loadimg("images/cases/openimgs/legendary.png")]
    images.cases = [loadimg("images/cases/case-first_class.png"),
             loadimg("images/cases/case-alien_class.png")]
    images.selected = loadimg('images/cases/selected.png')
    images.case0 = [loadimg("images/skins/human_case/st1.png"),
             loadimg("images/skins/human_case/st2.png"),
             loadimg("images/skins/human_case/st3.png"),
             loadimg("images/skins/human_case/st4.png"),
             loadimg("images/skins/human_case/st5.png"),
             loadimg("images/skins/human_case/st6.png"),
             loadimg("images/skins/human_case/st7.png"),
             loadimg("images/skins/human_case/st8.png"),
             loadimg("images/skins/human_case/st9.png"),
             loadimg("images/skins/human_case/st10.png"),
             loadimg("images/skins/human_case/st11.png"),
             loadimg("images/skins/human_case/st12.png"),
             loadimg("images/skins/human_case/st13.png"),
             loadimg("images/skins/human_case/st14.png"),
             loadimg("images/skins/human_case/st15.png"),
             loadimg("images/skins/human_case/st16.png"),
             loadimg("images/skins/human_case/st17.png"),
             loadimg("images/skins/human_case/st18.png")]
             

    images.case1 = [loadimg("images/skins/alien_case/st1.png"),
             loadimg("images/skins/alien_case/st2.png"),
             loadimg("images/skins/alien_case/st3.png"),
             loadimg("images/skins/alien_case/st4.png"),
             loadimg("images/skins/alien_case/st5.png"),
             loadimg("images/skins/alien_case/st6.png"),
             loadimg("images/skins/alien_case/st7.png"),
             loadimg("images/skins/alien_case/st8.png"),
             loadimg("images/skins/alien_case/st9.png"),
             loadimg("images/skins/alien_case/st10.png"),
             loadimg("images/skins/alien_case/st11.png"),
             loadimg("images/skins/alien_case/st12.png"),
             loadimg("images/skins/alien_case/st13.png"),
             loadimg("images/skins/alien_case/st14.png"),
             loadimg("images/skins/alien_case/st15.png"),
             loadimg("images/skins/alien_case/st16.png"),
             loadimg("images/skins/alien_case/st17.png"),
             loadimg("images/skins/alien_case/st18.png")]

    images.case_background = loadimg("images/cases/background.png")
    images.death = loadimg("images/death.png")
    images.shop = loadimg("images/shop.png")
    images.leader = loadimg("images/leader.png")
    images.buy = loadimg("images/buy.png")

#load_images()
