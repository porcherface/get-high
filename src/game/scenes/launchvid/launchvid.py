#!/usr/bin/env python3
import os
import pygame 

from typing import Tuple

import game.lib.scene as libs

import random
import pathlib
launchvidpath = pathlib.Path(__file__).parent.absolute()


def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio

class LaunchvidScene(object):
    def __init__(self):
        self.STATE = 0
        self.fps = 40
        libs.Scene.__init__(self)
        backdroppath=os.path.join(launchvidpath,'res','redconiglio.png')


        self.worldx = 1376
        self.worldy= 768
        self.camx = 1376
        self.camy= 768
        self.world =  pygame.display.set_mode([self.camx, self.camy])
        self.backdrop = pygame.image.load(os.path.join(backdroppath)).convert()
        self.backdropbox = self.backdrop.get_rect()
        self.clock = pygame.time.Clock()


        self.backsback=pygame.Surface([self.camx, self.camy]).convert()
        self.backsback.fill([0,0,0])
        pygame.display.flip()
        musicpath = os.path.join(launchvidpath,'res','valve.mp3')

        if MY_AUDIO_IS_WORKING:
            pygame.mixer.music.load(musicpath)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.2)

        t0 = pygame.time.get_ticks()
        print(t0)
        delay_time = 12000

        main1 = True
        main2 = True
        while main1 and main2:
            
            t1 =pygame.time.get_ticks()
            main2 = ((t1-t0)< delay_time)
            main1 = self.handle_events(pygame.event.get())
            self.update(t1-t0)       
            self.render()     

            
    def render(self):

        pygame.display.flip()
        self.clock.tick(self.fps)

    def update(self,tick_count):

        this_alpha = 255
        if tick_count < 4000:
            this_alpha = int(255 - (4000-tick_count)*255/4000)
           
        if tick_count > 8000:
            this_alpha = int(255-(tick_count-8000)*255/4000)
        
        if this_alpha > 255:
            this_alpha = 255

        self.backdrop.set_alpha(this_alpha,0) #a number from 0 to 255

        self.world.blit(self.backsback, self.backsback.get_rect())
        self.world.blit(self.backdrop, self.backdropbox)

    def handle_events(self, events):
        
        main = True
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main = False

        return main
