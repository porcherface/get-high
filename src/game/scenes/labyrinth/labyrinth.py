#!/usr/bin/env python3

from typing import Tuple

import pygame
import sys
import os

import game.lib.player as libp
import game.lib.button as libb
import game.lib.scene as libs
import game.lib.enemy as libe
import game.lib.camera as libc
import game.lib.terrain as libt

import random
import pathlib
labyrinthpath = pathlib.Path(__file__).parent.absolute()



def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio
    

class LabyrinthScene(libs.Scene):
    def __init__(self):

        print("hello maze!")

        self.STATE = 0
        libs.Scene.__init__(self)
        backdroppath=os.path.join(labyrinthpath,'res','bg_maze.png')
        self.fps = 40
        self.worldx = 2048
        self.worldy= 1024
        self.camx = 1376
        self.camy= 768
        self.world = pygame.display.set_mode([self.camx, self.camy])
        self.clock = pygame.time.Clock()

        #get elapsed time using this!
        #elapsed_time = pygame.time.get_ticks()
        
        self.player_list =[]
        self.player1 = libp.SpaceShip(1)
        self.player2 = libp.SpaceShip(2)


        self.camera = libc.Camera(self.camx,self.camy,self.worldx, self.worldy,libc.blinking_camera)

        self.player1.rect.x = self.worldx * 1/10
        self.player2.rect.x = self.worldx * 9/10

        self.player1.rect.y = self.worldy * 9/10
        self.player2.rect.y = self.worldy * 1/10

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player1)
        self.player_list.add(self.player2)

        self.focused_player = self.player1

        self.backdrop = pygame.image.load(os.path.join(backdroppath)).convert_alpha()
        self.backdropbox = self.backdrop.get_rect()



        #maybe we can also load from file
        #MAYBE:....
        self.level_map = [    
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X         x    x      x                x         x             X",
        "X         b    x      x                x         x         2   X",
        "X         b    x      x           x    x    x    x             X",
        "X         x    x      xxxxxxx     x         x    x             X",
        "X     xxxxxbbbbx      r           x         x    x             X",
        "X     x        r      r        xxxxrrrxxxxxxxbbbbx             X",
        "X     x        r      r        x        x        x             X",
        "X     xxxxxxxxxxxxxxxxxxxbbbbbxx        x                      X",
        "X              b      r        xxxrrrrxxx                      X",
        "X              b      r           b      xrrrrxxxxxxxxxxxxxxxxxX",
        "Xxxxxx         x      r           b      x                     X",
        "X            xxxxxxxxxxxxxxxxxxxxxxx     x             xxx     X",
        "X                         r     x        x      xx             X",
        "X                         r     x        x              x      X",
        "X            xxxxxxxxxxxxxxx    x        x                     X",
        "X      xxxxxxx        x         x        x         xxx         X",
        "X                     x         x        x                     X",
        "X                     x    xxxxxx        xxxxxxxxxxxxxxx       X",
        "X                     x    x    x        x                     X",
        "Xxxrrrrxxxxxx         x    b    x   xxxxxx                     X",
        "X         x                b    x        x                     X",
        "X         x      x         b    x        x        xxxxxxxxxxxxxX",
        "Xbbbbbx   xrrrrrxxxxxxxxxxxx    x       x                     xX",
        "X     x   x      x        x     x                  x           X",
        "X     x   x      x        x     x                 xxx          X",
        "X     x   x               x     x                 xxx          X",
        "X     x                   x     xxxxxxxxxxxxxx    xxx          X",
        "X  1  x                   x       x             xxx xxx        X",
        "X     x                   b       x             xxx xxx        X",
        "X     x                   b       x                            X",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]


        self.map_specs = ["64x32","32x32","2048x1024"]
        self.terrain_group = pygame.sprite.Group()
        self.special_group = pygame.sprite.Group()
        self.p1collision_group = pygame.sprite.Group()
        self.p2collision_group = pygame.sprite.Group()
        cx = 0
        cy = 0
        size = 32
        for row in self.level_map:
            cx=0
            for char in row:
                if char == "x" or char == "X":
                    thisblock = libt.Block(cx*size,cy*size)
                    self.terrain_group.add(thisblock)
                    self.p1collision_group.add(thisblock)
                    self.p2collision_group.add(thisblock)

                if char == "1":
                    self.player1.rect.x = cx*size
                    self.player1.rect.y = cy*size
                if char == "2":
                    self.player2.rect.x = cx*size
                    self.player2.rect.y = cy*size
                if char == "b":
                    thisblock = libt.Block(cx*size,cy*size,(0,0,250))
                    self.special_group.add(thisblock) 
                    self.p2collision_group.add(thisblock)
                if char == "r":
                    thisblock = libt.Block(cx*size,cy*size,(250,0,0))
                    self.special_group.add(thisblock) 
                    self.p1collision_group.add(thisblock)
                cx+=1
            cy+=1            
        
#        if self.player1.check_collision_simple(self.enemy_list):     

        '''
        Main Loop
        '''
        main = True
        self.respawn_bugfix = False
        while main:


            main = self.handle_events(pygame.event.get())    
            main = self.update()
            self.render()

            main = self.reunite()
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

        for block in self.terrain_group:
            self.world.blit(block.image,f(block.rect))

        for block in self.special_group:
            self.world.blit(block.image,f(block.rect))

        self.clock.tick(self.fps)
        pygame.display.update()
        pygame.display.flip()
        
    def update(self):
        self.player1.update_2(self.p1collision_group)
        self.player2.update_2(self.p2collision_group)
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
                    self.player2.showchat(1)    

                if event.key == ord('f'):
                    self.focused_player = self.player1

                if event.key == ord('.'):
                    self.focused_player = self.player2

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
                    self.player2.showchat(0)

        return main


