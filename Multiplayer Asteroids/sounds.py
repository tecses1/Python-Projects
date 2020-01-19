import pygame
pygame.mixer.init()
menu_song = pygame.mixer.Sound("snd/music/song_menu.ogg")
paused_song = pygame.mixer.Sound("snd/music/song_paused.ogg")
battle_song = pygame.mixer.Sound("snd/music/song_battle.ogg")
purchased = pygame.mixer.Sound("snd/sfx/purchased.wav")
asteroid_death = pygame.mixer.Sound("snd/sfx/asteroid_death.wav")
laser_shot = pygame.mixer.Sound("snd/sfx/shot.wav")
click = pygame.mixer.Sound("snd/sfx/menuclick.wav")
