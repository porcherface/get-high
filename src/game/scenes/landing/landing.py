#!/usr/bin/env python3
import os
import pygame 

from typing import Tuple

import pygame
import sys
import os

import game.lib.player as libp
import game.lib.button as libb
import game.lib.scene as libs
import game.lib.enemy as libe
import game.lib.camera as libc

import random
import pathlib
landingpath = pathlib.Path(__file__).parent.absolute()

######
# taking this level
# as a tutorial for camera movement implementation

# base code is taken from
# https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame
#
# camera will move only vertycally in this stage

    
class LandingScene(libs.Scene):
    def __init__(self):

        # pic is 1376, world is 1600, 
        # a black border is totally fine
        libs.Scene.__init__(self,1600, 7680)
        backdroppath=os.path.join(landingpath,'res','landing_background.png')
        
        self.backdrop = pygame.image.load(os.path.join(backdroppath))
        self.backdropbox = self.backdrop.get_rect()

        # not using these for now
        self.backsback=pygame.Surface([self.camx, self.camy]).convert()
        self.backsback.fill([0,0,0])
        

        #custom camera here!
        self.camera = libc.Camera(self.camx,self.camy,self.worldx, self.worldy, libc.chasing_camera)
        self.clock = pygame.time.Clock()
        
        self.player1 = libp.SpaceShip(1)
        self.player2 = libp.SpaceShip(2)

        self.player1.fuel = 100000
        self.player2.fuel = 100000

        self.player1.rect.x= self.worldx /3
        self.player1.rect.y= 100

        self.player2.rect.x= self.worldx /3 *2
        self.player2.rect.y= 100


        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player1)
        self.player_list.add(self.player2)
        
        self.player1.angle = 180
        self.player2.angle = 180

        
        main=True

        #if i put this here fall is constant
        fall1  = 15
        fall2  = 15
        self.player1.control(0,fall1)
        self.player2.control(0,fall2)

        self.rewspawn_bugfix = False
        while main:
            main = self.handle_events(pygame.event.get())    
            main = self.update()
            self.render()

        self.STATE = 0
        return

    def render(self):
        f = self.camera.apply
        self.world.blit(self.backsback, self.backdropbox )
        self.world.blit(self.backdrop, f(self.backdropbox))#self.camera.apply(self.backdropbox))#self.camera.apply(self.backdropbox))
        self.world.blit(self.player1.image, f(self.player1.rect))#self.camera.apply(self.player1.rect))
        self.world.blit(self.player2.image, f(self.player2.rect))#self.camera.apply(self.player2.rect))

        self.clock.tick(self.fps)
        pygame.display.update()
        pygame.display.flip()
        
    def update(self):

        self.player1.update([self.worldx,self.worldy])
        self.player2.update([self.worldx,self.worldy])
        self.camera.update(self.player2.rect)
        
        #self.world.blit(self.backdrop, self.camera.apply(self.backdropbox))
        #self.world.blit(self.backdrop, self.camera.apply(self.player1.rect))
        
        #reached end of screen
        if(self.player2.rect.y > 7600):
            return False

        return True

    def handle_events(self, events):
        main = True
       
        steps1 = self.player1.speed
        steps2 = self.player2.speed
        fall1  = 1.01
        fall2  = 1.1

        # if i put control here it accelerates! (integration!)
        #self.player1.control(0,fall1)

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.type == pygame.KEYDOWN:
                self.rewspawn_bugfix = True
                
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
                
             
            if event.type == pygame.KEYUP and self.rewspawn_bugfix:
                if event.key == ord('a'):
                    self.player1.control(steps1, 0)
                if event.key == pygame.K_LEFT:
                    self.player2.control(steps2, 0)
                if event.key == ord('d'):
                    self.player1.control(-steps1, 0)
                if event.key == pygame.K_RIGHT:
                    self.player2.control(-steps2, 0)


        return main
