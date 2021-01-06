#!/usr/bin/env python3
import os
import pygame

class Camera(object):
    def __init__(self, width, height,worldx, worldy,camera_func = None):
        self.camera_func = camera_func
        self.rect = pygame.Rect(0, 0, width, height)
        self.worldx = worldx
        self.worldy = worldy

    def apply(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def update(self, target_rect):
        self.rect = self.camera_func(self.rect, target_rect, [self.worldx,self.worldy])
    
    #simple attachable chasing camera
    #can follow ANY sprite spawned
def chasing_simple_camera(camera_rect, target_rect, world_xy):
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera_rect     # w = width, h = height
    return pygame.Rect(-l+w/2, -t+h/2, w, h)

def chasing_camera(camera_rect, target_rect,world_xy):

    outcamera = camera_rect
    w = camera_rect.width
    h= camera_rect.height

    # we want to center target_rect
    x = -target_rect.center[0] + w/2 
    y = -target_rect.center[1] + h/3
    # this is where "simple_camera ends"
    #if i return
    #return pygame.Rect(x,y, w, h)
    # the effect is exactly the same
    
    # move the camera. Let's use some vectors so we can easily substract/multiply
    outcamera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera_rect.topleft)) * 0.06 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    outcamera.x = max(-(world_xy[0]-camera_rect.width), min(0, outcamera.x))
    outcamera.y = y#max(-(world_xy[1]-camera_rect.height), min(0, outcamera.y))#y
    
    return outcamera
def double_chasing_camera(camera_rect, target_rect,world_xy):

    outcamera = camera_rect
    w = camera_rect.width
    h= camera_rect.height

    # we want to center target_rect
    x = -target_rect.center[0] + w/2 
    y = -target_rect.center[1] + h/3
    # this is where "simple_camera ends"
    #if i return
    #return pygame.Rect(x,y, w, h)
    # the effect is exactly the same
    
    # move the camera. Let's use some vectors so we can easily substract/multiply
    outcamera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera_rect.topleft)) * 0.06 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    outcamera.x = max(-(world_xy[0]-camera_rect.width), min(0, outcamera.x))
    outcamera.y = max(-(world_xy[1]-camera_rect.height), min(0, outcamera.y))#y    
    return outcamera

#def static_camera()
def blinking_camera(camera_rect, target_rect,world_xy):

    outcamera = camera_rect
    w = camera_rect.width
    h= camera_rect.height

    # we want to center target_rect
    x = -target_rect.center[0] + w/2 
    y = -target_rect.center[1] + h/2
    # this is where "simple_camera ends"
    #if i return
    #return pygame.Rect(x,y, w, h)
    # the effect is exactly the same
    
    
    # move the camera. Let's use some vectors so we can easily substract/multiply
    outcamera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera_rect.topleft)) * 1 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    outcamera.x = max(-(world_xy[0]-camera_rect.width), min(0, outcamera.x))
    outcamera.y = max(-(world_xy[1]-camera_rect.height), min(0, outcamera.y))
    
    return outcamera
        