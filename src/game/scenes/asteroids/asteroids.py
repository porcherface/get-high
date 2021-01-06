#!/usr/bin/env python3

from typing import Tuple

import pygame
import sys
import os

import game.lib.player as libp
import game.lib.button as libb
import game.lib.scene as libs
import game.lib.enemy as libe
import random
import pathlib
asteroidpath = pathlib.Path(__file__).parent.absolute()

ASTEROID_TIME_VAL = 1000

def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio

class AsteroidScene(libs.Scene):
    def __init__(self,autorun=True):
        print("AsteroidScene")

        libs.Scene.__init__(self)
        backdroppath=os.path.join(asteroidpath,'res','space_bg_sara.png')
        

        self.hardener = 10

        #get elapsed time using this!
        #elapsed_time = pygame.time.get_ticks()
        self.player_list =[]
        self.player1 = libp.SpaceShip(1)
        self.player2 = libp.SpaceShip(2)
        self.player_dead = False
        
        self.player1.rect.x = self.worldx/3
        self.player2.rect.x = self.worldx*2/3

        self.player1.rect.y = self.worldy/2
        self.player2.rect.y = self.worldy/2

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player1)
        self.player_list.add(self.player2)

        self.backdrop = pygame.transform.scale(pygame.image.load(os.path.join(backdroppath)), (self.worldx, self.worldy) )
        self.backdropbox = self.world.get_rect()
 

        self.surviveLabel = libb.Label("survive")
        self.surviveLabel.position(self.worldx/2,self.worldy/2)
        

        self.timer = libb.Timer(pygame.time.get_ticks())
        self.timer.position(self.worldx/2, 30)


        '''
        Main Loop
        '''
        self.t0 = pygame.time.get_ticks()
        self.delay_time = 2000
  
        if autorun:

            main1 = True
            main2 = True

            self.enemy_list = pygame.sprite.Group()
            self.yum_list =  pygame.sprite.Group()
            self.asteroid_count = 0
            self.ASTEROID_EVENT_KEY =  pygame.USEREVENT + 1
            self.ASTEROID_EVENT = pygame.event.Event(self.ASTEROID_EVENT_KEY)
            

            self.DEATH_EVENT_KEY = pygame.USEREVENT +2
            self.DEATH_EVENT = pygame.event.Event(self.DEATH_EVENT_KEY)
            self.timer_set = False
            #pygame.event.post(ASTEROID_EVENT)
            pygame.time.set_timer(self.ASTEROID_EVENT_KEY, ASTEROID_TIME_VAL)

            #this avoids that bad flickering 
            self.rewspawn_bugfix = False

            self.timer.start(pygame.time.get_ticks() )
            while main1 and main2:
                self.t1 =pygame.time.get_ticks()
                main1 = self.handle_events(pygame.event.get())    
                main2 = self.update()
                self.render()

            return 
        #pygame.quit()
       
         
        
            

    def render(self):
        self.world.blit(self.backdrop, self.backdropbox)
        if (self.t1-self.t0)< self.delay_time or self.timer_set :
            self.surviveLabel.draw(self.world)

        self.timer.draw(self.world,pygame.time.get_ticks() )
        #self.player_list.draw(self.world)
        self.player1.draw(self.world)
        self.player2.draw(self.world)
        self.enemy_list.draw(self.world)
        self.yum_list.draw(self.world)

        self.player1.drawhud(self.world)
        self.player2.drawhud(self.world)

        pygame.display.update()
        #pygame.display.flip()
        self.clock.tick(self.fps)

    def update(self):
        self.player1.update([self.worldx,self.worldy])
        self.player2.update([self.worldx,self.worldy])

        for enemy in self.enemy_list:
            #print("updating "+enemy.id)
            enemy.update()
            if enemy.rect.x < -50 or enemy.rect.x > self.worldx+50:#outofbox(enemy):
                if enemy.rect.y < -50 or enemy.rect.y > self.worldy+50:#outofbox(enemy):
                
                    enemy.die()

        # check collision with players
        if self.player1.check_collision_simple(self.enemy_list):     
            # DEAD
            self.player1.die()
            self.player_dead = True
            self.timer.stop(pygame.time.get_ticks() )

            #return False
        if self.player2.check_collision_simple(self.enemy_list):
            # DEAD
            self.player2.die()
            self.player_dead = True
            self.timer.stop(pygame.time.get_ticks() )
            #return False
 
        if self.player1.check_collision_simple(self.yum_list):     
            self.player1.fuel+= 200
            if self.player1.fuel> 300:
                self.player1.fuel = 300
            
            cup = self.player1.check_collision_simple(self.yum_list)
            self.yum_list.remove(cup)
            cup.die()

        if self.player2.check_collision_simple(self.yum_list):
            self.player2.fuel+= 200
            if self.player2.fuel> 300:
                self.player2.fuel = 300

            cup = self.player2.check_collision_simple(self.yum_list)
            cup.die()
            self.yum_list.remove(cup)
        return True

    #100111001

    def handle_events(self, events):
        main = True
        steps1 = self.player1.speed
        steps2 = self.player2.speed

        for event in events:

            if self.player_dead and self.timer_set is False:
                pygame.time.set_timer(self.DEATH_EVENT_KEY,3000,True)
                self.timer_set = True

                self.surviveLabel = libb.Label("gameover")
                self.surviveLabel.position(self.worldx/2,self.worldy/2)

            if event.type == self.DEATH_EVENT_KEY:
                main = False
                self.STATE = 1


            if event.type == self.ASTEROID_EVENT_KEY:
                self.enemy_list.add(self.SpawnAsteroid(self.hardener))
                self.hardener+=1
                
                if self.hardener%10 == 4:
                    self.yum_list.add(self.SpawnCupCake(self.hardener))

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
                    
                if event.key == ord('ò'):
                    self.player2.showchat(1)    
                
                if event.key == ord('r'):
                    self.player1.interact()

                if event.key == ord('-'):
                    self.player2.interact()


            if event.type == pygame.KEYUP and self.rewspawn_bugfix:


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
                if event.key == ord('ò'):
                    self.player2.showchat(0)
                if event.key == ord('r'):
                    self.player1.interact(False)

                if event.key == ord('-'):
                    self.player2.interact(False)

        return main

    def SpawnAsteroid(self,count):
        
        
        sx= self.worldx + 30
        sy= -30
        outlist =[]
        for i in range(int(count/20)+1):
            outlist.append( libe.Asteroid( str(self.asteroid_count), [[sx,sy],[-10*random.random()+0.5,10*random.random()+0.5]]) )
            self.asteroid_count+=1
            outlist.append( libe.Asteroid(str(self.asteroid_count),[[-25,random.random()*self.worldy],[10*random.random()+0.5,1*random.random()-0.5]]) )    
            self.asteroid_count+=1
        return outlist


    def SpawnCupCake(self,count):
        
        
        sx= self.worldx*random.random()
        sy= self.worldy*random.random()
 
        cuppy= libe.CupCake( "cup"+str(count), [[sx,sy],[0,0]]) 
        return cuppy
r'''
      (\__/) 
      (•ㅅ•)      my gf telling the waitress
   ＿ノ ヽ ノ＼__   my food is wrong
 /　`/ ⌒Ｙ⌒ Ｙ　ヽ     
( 　(三ヽ人　 /　 |     
|　ﾉ⌒＼ ￣￣ヽ　 ノ    
ヽ＿＿＿＞､＿＿_／ 
　　 ｜( 王 ﾉ〈 (\__/) 
　　 /ﾐ`ー―彡\  (•ㅅ•)  me
'''
