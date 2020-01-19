import pygame
import network_classes
import game_classes
import sys
import select
import funct
class main():
    def __init__(self,host):
        if host:
            server = network_classes.Server((funct.savedata[3],funct.savedata[4]))
            pygame.display.quit()
            while True:
                try:
                    server.update()
                except KeyboardInterrupt:
                    sys.exit()
        else:
            screen = pygame.display.set_mode((800,600))
            localPlayer = pygame.sprite.GroupSingle()
            localPlayer.add(game_classes.localPlayer(screen))
            fps_clock = pygame.time.Clock()
            while True:
                screen.fill((0,0,0))
                fps_clock.tick(60)
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_c:
                            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                pygame.display.quit()
                                
                localPlayer.update()
                pygame.display.flip()
