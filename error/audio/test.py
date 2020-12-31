

import os
import pygame
import pathlib

filepath = pathlib.Path(__file__).parent.absolute()

#bunch of inits
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
pygame.mixer.init()


musicpath = os.path.join(filepath,'valve.mp3')

pygame.mixer.music.load(musicpath)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)

main = True

while main:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main = False
