#!/usr/bin/env python3

# flares
#

from typing import Tuple
import pygame
import sys
import os

import game.lib.player as libp
import game.lib.button as libb
import game.lib.scene as libs
import game.lib.camera as libc

import pathlib
flarepath = pathlib.Path(__file__).parent.absolute()


'''
global Variables
''' 

class FlaresScene(libs.Scene):
    def __init__(self, chosen_one = 1):

        libs.Scene.__init__(self, 2048, 1024)
        #WARNING THIS IS STOLEN AND MUST BE REPLACED
        backdroppath=os.path.join(flarepath,'res','jungle_stolen.jpg')

        self.player_list =[]

        if chosen_one == 1:
            self.player1 = libp.Pilot(1)
            self.player2 = libp.CrossHair(2)
            self.focused_player = self.player1

        else:            
            self.player1 = libp.CrossHair(1)
            self.player2 = libp.Pilot(2)
            self.focused_player = self.player2


        self.camera = libc.Camera(self.camx,self.camy,self.worldx, self.worldy,libc.chasing_camera)

        ''' WE DONT NEED THESE ANYMORE 
        self.player1.rect.x = self.worldx * 1/10
        self.player2.rect.x = self.worldx * 9/10
        self.player1.rect.y = self.worldy * 9/10
        self.player2.rect.y = self.worldy * 1/10
        '''

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player1)
        self.player_list.add(self.player2)

        self.focused_player = self.player1

        self.backdrop = pygame.image.load(os.path.join(backdroppath)).convert_alpha()
        self.backdropbox = self.backdrop.get_rect()


        '''
        Main Loop
        '''
        main = True
        self.respawn_bugfix = False
        while main:


            main = self.handle_events(pygame.event.get())    
            main = self.update()
            self.render()

            #main = self.reunite()
        return 
        #pygame.quit()

    def reunite(self):

        deltax = self.player1.rect.x - self.player2.rect.x
        deltay = self.player1.rect.y - self.player2.rect.y

        sq_tol = 400
        if(deltax*deltax + deltay*deltay >sq_tol):
            return True

        return False


    def render(self):
        f = self.camera.apply
        self.world.blit(self.backdrop, f(self.backdropbox))#self.camera.apply(self.backdropbox))#self.camera.apply(self.backdropbox))
        self.world.blit(self.player1.image, f(self.player1.rect))#self.camera.apply(self.player1.rect))
        self.world.blit(self.player2.image, f(self.player2.rect))#self.camera.apply(self.player2.rect))
        self.clock.tick(self.fps)
        pygame.display.update()
        pygame.display.flip()
        
    def update(self):
        self.player1.update([self.worldx,self.worldy])
        self.player2.update([self.worldx,self.worldy])
        self.camera.update(self.focused_player.rect)
        
        return True

    def handle_events(self, events):
        main = True
        walk_speed = 10
        steps1 = walk_speed
        steps2 = walk_speed


        for event in events:
 
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.type == pygame.KEYDOWN:

                self.respawn_bugfix = True
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
                    pass
                    #self.player2.current_cross+=1

            if event.type == pygame.KEYUP and self.respawn_bugfix:


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
                    #if self.has_pressed:
                    self.player2.current_cross = (self.player2.current_cross+1) % 8
                    #self.player2.current_cross+=1

        return main


