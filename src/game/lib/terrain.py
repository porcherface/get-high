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

class Block(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self,posx,posy,block_type=None, size=32):
 
        pygame.sprite.Sprite.__init__(self)
        self.type = block_type
        
        self.posx = posx
        self.posy = posy

        self.size = size
        self.rect = pygame.Rect(posx,posy,size,size)
 
        if block_type == None:
            self.image = pygame.Surface([size,size])
            self.image.fill([120,120,120])
        else:
            self.image = pygame.Surface([size,size])
            self.image.fill(block_type)
            

class Terrain(pygame.sprite.Group):
    def __init__(self,enemy_type=None, size=None):
        pygame.sprite.Group.__init__(self)