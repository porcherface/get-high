

import os
import pygame
import pathlib

filepath = pathlib.Path(__file__).parent.absolute()

#bunch of inits
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
pygame.mixer.init()

good = 0
try:    
    musicpath = os.path.join(filepath,'valve.mp3')
    pygame.mixer.music.load(musicpath)
    good += 1
    print("mp3 passed")
except:
    print("mp3 failed")
try:    
    musicpath = os.path.join(filepath,'valve.ogg')
    pygame.mixer.music.load(musicpath)
    good += 1
    print("ogg passed")
except:
    print("ogg failed")
try:    
    musicpath = os.path.join(filepath,'valve.wav')
    pygame.mixer.music.load(musicpath)
    good += 1
    print("wav passed")
except:
    print("wav failed")
    
if good == 3:
    print("[ OK ]")
elif good > 0:
    print("[pass]")
else:
    print("[FAIL]")

print("Press SPACEBAR to stop...")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)

main = True

while main:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main = False
