#!/usr/bin/env python3

# title scene:
# new game / load game buttons, 

from typing import Tuple

import pygame
import sys
import os

import game.lib.player as libp
import game.lib.button as libb
import game.lib.scene as libs

import pathlib
titlepath = pathlib.Path(__file__).parent.absolute()


'''
global Variables
'''


def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio

    

class LoadWindow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load(os.path.join(titlepath,'res','loadwindow.png') )
        self.boundingbox = self.image.get_rect()  
        self.level_boundbox = self.image.get_rect()
        #sprite prop
        self.boundingbox.x += 100
        self.boundingbox.y += 400

        self.level_list = []

        #level_1 = libb.Button("asteroid")
        level_1 = libb.Button()
        
        level_1.set_interaction_box(self.level_boundbox)
        self.level_list.append(level_1)



class TitleScene(libs.Scene):
    def __init__(self):
        self.STATE = 0
        libs.Scene.__init__(self)
        backdroppath=os.path.join(titlepath,'res','title_background.jpg')
        musicpath = os.path.join(titlepath,'res','borntodie_instr.ogg')
        

        self.fps = 40
        self.worldx = 1376
        self.worldy = 768
        self.world = pygame.display.set_mode([self.worldx, self.worldy])
        self.clock = pygame.time.Clock()

        if MY_AUDIO_IS_WORKING:
            pygame.mixer.music.load(musicpath)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)

        self.backdrop = pygame.image.load(os.path.join(backdroppath))
        self.backdropbox = self.world.get_rect()

        self.player1 = libp.SpaceShip(1)  # spawn player
        self.player2 = libp.SpaceShip(2)  # spawn player

        self.player1.rect.x = 300  # go to x
        self.player1.rect.y = 500  # go to y
        self.player2.rect.x = 600
        self.player2.rect.y = 500

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player1)
        self.player_list.add(self.player2)

        self.entity_list = pygame.sprite.Group()
        self.entity_list.add(self.player1.baloon)
        self.entity_list.add(self.player2.baloon)

        self.startbutton = libb.Button("startbutton")
        self.loadbutton = libb.Button("loadlevel")
        #cmdsbutton = libb.Button("commands.png")

        self.startbutton.rect.x = self.worldx / 2 +160
        self.startbutton.rect.y = self.worldy / 2 
        self.loadbutton.rect.x = self.worldx / 2 + 160
        self.loadbutton.rect.y = self.worldy / 2 + 80

        self.button_list = pygame.sprite.Group()
        self.button_list.add(self.startbutton)
        self.button_list.add(self.loadbutton)

        self.loadwindow = LoadWindow()


        '''
        Main Loop
        '''
        main = True
        while main:
            main = self.handle_events(pygame.event.get())    
            main = self.update()
            self.render()

        #pygame.quit()


    def render(self):
        self.entity_list.draw(self.world)
        self.button_list.draw(self.world)
        self.player_list.draw(self.world)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def update(self):
        self.world.blit(self.backdrop, self.backdropbox)
        
        self.player1.update([self.worldx,self.worldy])
        self.player2.update([self.worldx,self.worldy])
        for button in self.button_list:
            button.update()

            if button.triggered == True:
                if button.name == "loadlevel":
                    
                    # I AM TRYING TWO METHODS TO LOAD A LOADWINDOW

                    #self.loadwindow.draw(self.world)
                    self.world.blit(self.loadwindow.image, self.loadwindow.boundingbox)
                    
                    if True: #will substitute it with loadlevel logic
                        self.STATE = 1
                        print("state 1 print")
                        return False
                        
                    #return False


                if button.name == "startbutton":
                    self.STATE = 0
                    return False
        return True

    def handle_events(self, events):
        main = True
        steps1 = self.player1.speed
        steps2 = self.player2.speed

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False

            # we want to incorporate this later in the SpaceShip class!!!

            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False


                if event.key == ord('a'):
                    self.player1.control(-steps1, 0)
                if event.key == pygame.K_LEFT:
                    self.player2.control(-steps2, 0)
                
                if event.key == ord('d'):
                    self.player1.control(steps1, 0)
                if event.key == pygame.K_RIGHT:
                    self.player2.control(steps2, 0)
                
                if event.key == ord('w'):
                    self.player1.control(0,-steps1)
                if event.key == pygame.K_UP:
                    self.player2.control(0, -steps2)
                
                if event.key == ord('s'):
                    self.player1.control(0,steps1)
                if event.key == pygame.K_DOWN:
                    self.player2.control(0, steps2)

                if event.key == ord('e'):
                    self.player1.showchat(1)
                    
                if event.key == ord('-'):
                    self.player2.showchat(1)    
                
                if event.key == ord('f'):
                    for button in self.button_list:
                        button.interact(self.player1)

                if event.key == ord('.'):
                    for button in self.button_list:
                        button.interact(self.player2)

            if event.type == pygame.KEYUP:
                if event.key == ord('a'):
                    self.player1.control(steps1, 0)
                if event.key == pygame.K_LEFT:
                    self.player2.control(steps2, 0)
                
                if event.key == ord('d'):
                    self.player1.control(-steps1, 0)
                if event.key == pygame.K_RIGHT:
                    self.player2.control(-steps2, 0)
                
                if event.key == ord('w'):
                    self.player1.control(0,steps1)
                if event.key == pygame.K_UP:
                    self.player2.control(0, steps2)
                
                if event.key == ord('s'):
                    self.player1.control(0,-steps1)
                if event.key == pygame.K_DOWN:
                    self.player2.control(0,-steps2)
                
                if event.key == ord('e'):
                    self.player1.showchat(0)
                if event.key == ord('-'):
                    self.player2.showchat(0)

        return main

    def bound_to_world(self):

        if self.player1.x<0:
            self.player1.x=0
        if self.player1.y<0:
            self.player1.y=0

        if self.player1.x>self.worldx:
            self.player1.x=self.worldy
        if self.player1.y>self.worldy:
            self.player1.y=self.worldy
        
        if self.player2.x<0:
            self.player2.x=0
        if self.player2.y<0:
            self.player2.y=0

        if self.player2.x>self.worldx:
            self.player2.x=self.worldy
        if self.player2.y>self.worldy:
            self.player2.y=self.worldy
