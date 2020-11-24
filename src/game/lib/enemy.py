#!/usr/bin/env python3
import os
import pygame
import random

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

import pathlib
libpath = pathlib.Path(__file__).parent.absolute()



class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self,enemy_type=None, enemy_name=None):
 
        pygame.sprite.Sprite.__init__(self)
        self.id = enemy_name
        self.type = enemy_type
       
        self.is_valid = True

    def set_initial_conditions(self):
        raise NotImplementedError

    def die(self,condition=False):
        if condition:
            self.kill()

            
class CupCake(Enemy):
    
    def __init__(self,enemy_name,additional = None):
        Enemy.__init__(self,"cupcake",enemy_name)
        imgpath=os.path.join(libpath,'res','enemy', self.type+'.png')
        img = pygame.image.load(imgpath).convert_alpha()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  # set alpha
        self.image =img
        boundingbox = pygame.transform.rotate(self.image,45)
        self.rect = boundingbox.get_rect()


        # this is only temporary, will be substituted with structured data
        if additional != None:
            self.set_initial_conditions(additional[0],additional[1])

    def set_initial_conditions(self,xcouple,vcouple):

        self.rect.x = xcouple[0]
        self.rect.y = xcouple[1]
        self.movex = vcouple[0]
        self.movey = vcouple[1]
        
class Asteroid(Enemy):
    def __init__(self,enemy_name,additional = None):
        Enemy.__init__(self,"asteroid",enemy_name)


        self.movex = 0
        self.movey = 0
        self.angle = 0
        randval = random.randrange(3)
        imgpath=os.path.join(libpath,'res','enemy', self.type+"_"+str(randval)+'.png')
        img = pygame.image.load(imgpath).convert_alpha()
        img.convert_alpha()  # optimise alpha
        #img.set_colorkey(ALPHA)  # set alpha
        self.image =img
        self.original=self.image
        boundingbox = pygame.transform.rotate(self.image,45)
        self.rect = boundingbox.get_rect()

        # this is only temporary, will be substituted with structured data
        if additional != None:
            self.set_initial_conditions(additional[0],additional[1])

    def set_initial_conditions(self,xcouple,vcouple):

        self.rect.x = xcouple[0]
        self.rect.y = xcouple[1]
        self.movex = vcouple[0]
        self.movey = vcouple[1]
        
        self.angle = random.random()*360
        self.angle_speed = 3*(random.random()-0.5)
    
    def update(self):
        """
        Update sprite position
        """
        
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.angle = self.angle + self.angle_speed


        #WARNING; THIS IS REALLY HARDWARE CONSUMING???
        oldcenter = self.rect.center
        #self.image = pygame.transform.rotate(self.original, self.angle) 
        self.rect.center = oldcenter