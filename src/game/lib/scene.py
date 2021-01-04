#!/usr/bin/env python3
import os
import pygame 

from pygame.locals import FULLSCREEN as FULLSCREEN

class Scene(object):
    def __init__(self,x = None,y = None, rx = None, ry = None):

        if x == None or y == None:
            infoObject  = pygame.display.Info()
            x = infoObject.current_w
            y = infoObject.current_h

        if rx == None or ry == None:
            infoObject  = pygame.display.Info()
            rx = infoObject.current_w
            ry = infoObject.current_h

        self.STATE = 0
        self.fps = 40
        self.worldx = x
        self.worldy = y
        self.camx   = rx
        self.camy   = ry
        self.clock = pygame.time.Clock()
        self.world  = pygame.display.set_mode([self.camx, self.camy],FULLSCREEN)
        return

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

