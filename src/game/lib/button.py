#!/usr/bin/env python3
import os
import pygame
from typing import Tuple

import pathlib
libpath = pathlib.Path(__file__).parent.absolute()

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)


class Label(pygame.sprite.Sprite):
    def __init__(self, labelname=None):
        pygame.sprite.Sprite.__init__(self)
        if labelname != None:
            img = pygame.image.load(os.path.join(libpath,'res', 'buttons',labelname+'.png')).convert_alpha()
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.image = img
            self.imagebox =img.get_rect()

    def draw(self,world):
        world.blit( self.image , self.imagebox)      

    def position(self,x,y):
        self.imagebox.center = (x,y)

"""
                  .,-:;//;:=,
          . :H@@@MM@M#H/.,+%;,
       ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=             .---=-=:=,.
  =@#@@@MX.,                -%HX$$%%%:;
 =-./@M@M$                   .;@MMMM@MM:
 X@/ -$MM/                    . +MM@@@M$
,@M@H: :@:                    . =X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+..%#$.
 /MMMM@MMH/.                  XM@MH; =;
  /%+%$XHH@$=              , .H@@@@MX,
   .=--------.           -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@= =,
               =++%%%%+/:-.

    """

class Button(pygame.sprite.Sprite):
    def __init__(self, buttonicon=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
    
        self.has_p1 =False
        self.has_p2 =False
        self.name = buttonicon
        self.triggered = False

        if buttonicon != None:
            for item in ["","_1","_2","_both"]:
                img = pygame.image.load(os.path.join(libpath,'res', 'buttons',buttonicon+item+'.png')).convert_alpha()
                img.convert_alpha()  # optimise alpha
                img.set_colorkey(ALPHA)  # set alpha
                self.images.append(img)
                self.image = self.images[0]
                self.rect = self.image.get_rect()

                self.interaction_box = self.rect

    def set_interaction_box(self,rect_in):
        self.interaction_box = rect_in


    def update(self):

        if self.has_p1 and self.has_p2:
            self.image = self.images[3]
            self.triggered = True

        else:
            if self.has_p1:
                self.image = self.images[1]
            if self.has_p2:
                self.image = self.images[2]

    def interact(self,item):
        
        x = item.rect.center
        
        if self.interaction_box.topleft[0] < x[0] and self.interaction_box.bottomright[0]:
            if x[0] and self.interaction_box.topleft[1] <x[1] and self.interaction_box.bottomright[1]>x[1]:
                #print("interacting with "+item)
                if item.id == 1:
                    self.has_p1 = True
                if item.id == 2:
                    self.has_p2 = True


    def draw(self,world):

        world.blit( self.image , self.imagebox)



class Timer(pygame.sprite.Sprite):
    def __init__(self, labelname="timer",start_time=pygame.time.get_ticks()):
        pygame.sprite.Sprite.__init__(self)
 
        self.font = pygame.font.SysFont(None, 32)
        counting_seconds = str(0).zfill(2)
        counting_millisecond = str(0).zfill(3)
        counting_string = "%.2s:%.3s" % ( counting_seconds, counting_millisecond)
        self.counting_text = self.font.render(str(counting_string), 1, (255,255,255))
        self.counting_rect = self.counting_text.get_rect()
        self.is_going = True

    def position(self,x,y):
        self.counting_rect.center = (x,y)


    def start(self,start_time=pygame.time.get_ticks()):
        self.start_time = start_time
        self.is_going=True


    def stop(self,stop_time=pygame.time.get_ticks()):
        
        if self.is_going:
            self.counting_time = stop_time- self.start_time

    
        self.is_going=False

    def draw(self,world,counting_time):
 
        if self.is_going:
            self.counting_time = pygame.time.get_ticks() - self.start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_seconds = str( int(( self.counting_time)/1000) ).zfill(2)
        counting_millisecond = str( self.counting_time%1000).zfill(3)

        counting_string = "%.3s . %.3s" % ( counting_seconds, counting_millisecond)

        self.counting_text = self.font.render(str(counting_string), 1, (255,255,255) )
 
        world.blit( self.counting_text, self.counting_rect)

 