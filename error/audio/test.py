

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
    goodpath = musicpath
    print("ogg passed")
except:
    print("ogg failed")
try:    
    musicpath = os.path.join(filepath,'valve.wav')
    pygame.mixer.music.load(musicpath)
    good += 1
    goodpath = musicpath
    print("wav passed")
except:
    print("wav failed")
    
try:
    musicpath = os.path.join(filepath,'valve.jpg')
    pygame.mixer.music.load(musicpath)
    print("negative failed")
except pygame.error:
    good += 1
    print("negative passed")


if good == 4:
    print("[ OK ]")
elif good > 1:
    print("[pass]")
else:
    print("[HARD FAIL]")
    print("1) uninstall pygame: pip3 uninstall pygame")
    print("2) install sdl_mixer: ")
    print("   dnf install libsdl2-dev")
    print("   dnf install SDL_mixer")
    print("3)install pygame: pip3 install pygame")
    


print("do u hear valve music?")
pygame.mixer.music.load(goodpath)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(1)


input("press enter to go on")
pygame.mixer.music.stop()
try:
    explosion = pygame.mixer.Sound( os.path.join(filepath,"explosion_sfx.ogg") )
    explosion.play()
    print("did u hear an explosion?")
except:
    print("explosion_sfx load failed")

print("Press SPACEBAR to stop...")

main = True

while main:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main = False
