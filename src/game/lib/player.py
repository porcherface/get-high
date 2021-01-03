#!/usr/bin/env python3
import os
import pygame

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 255)


import pathlib
libpath = pathlib.Path(__file__).parent.absolute()


def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio

class Baloon(pygame.sprite.Sprite):
    def __init__(self,icon_id=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.image =pygame.image.load(os.path.join(libpath,'res', 'player','baloon.png')).convert_alpha()
        self.image.convert_alpha()  # optimise alpha
        self.image.set_colorkey(ALPHA)  # set alpha
        self.rect = self.image.get_rect()

    def draw(self,world):
        world.blit( self.image,self.rect) 

class Shadow(pygame.sprite.Sprite):
    def __init__(self,icon_id=None):
        pygame.sprite.Sprite.__init__(self)
        
        self.image =pygame.image.load(os.path.join(libpath,'res', 'player','action.png')).convert_alpha()
        self.image.convert_alpha()  # optimise alpha
        self.image.set_colorkey(ALPHA)  # set alpha
        self.rect = self.image.get_rect()

    def draw(self,world):
        world.blit( self.image,self.rect) 

class Hud(pygame.sprite.Sprite):

    def __init__(self,player_id=None,x = None, y = None):
        pygame.sprite.Sprite.__init__(self)

        if x == None and y == None:
            infoObject  = pygame.display.Info()
            self.SCREEN_X = infoObject.current_w
            self.SCREEN_Y = infoObject.current_h



        self.totfuel = 300

        img = pygame.image.load(os.path.join(libpath,'res', 'player','player'+str(player_id)+'_icon.png')).convert_alpha()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(ALPHA)  
        self.image = img     
        self.imagebox= self.image.get_rect()     
        self.id = player_id
        # position icon
        if player_id == 1:
           self.imagebox.x = 0 + 80
           self.imagebox.y = self.SCREEN_Y - 140- 20 #hardcoded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        if player_id == 2:
            self.imagebox.x = self.SCREEN_X-140 -80
            self.imagebox.y = self.SCREEN_Y - 140-20 #hardcoded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
        self.gaugeframe=pygame.Surface([self.totfuel, 40]).convert()
        self.gauge=pygame.Surface([self.totfuel, 30]).convert()

        self.gaugeframe.fill([250,253,248])
        self.gauge.fill([250,1,5])

        self.gaugerect = self.gauge.get_rect()
        self.gaugeframerect = self.gaugeframe.get_rect()

        self.gaugeframerect.y = self.SCREEN_Y - 65
        self.gaugerect.y = self.SCREEN_Y - 60

        if player_id == 1:
            self.gaugeframerect.x = 0 + 80 + 140 
            self.gaugerect.x = 0 + 80 + 140  #hardcoded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if player_id == 2:       
            self.gaugeframerect.x = self.SCREEN_X - 140 - 80 - self.totfuel 
            self.gaugerect.x = self.SCREEN_X - 140 - 80 - self.totfuel  #hardcoded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def draw(self, world,params):



        # WARNING !!!! I SUSPECT THESE LINES ARE HIGHLY SUBOPTIMAL
        if params > 0:
            self.gauge=pygame.Surface([params, 30]).convert()
            self.gauge.fill([250,1,5])
            #self.gaugerect = self.gauge.get_rect()
            self.gaugerect.width = params

        if self.id  == 2:
            self.gaugerect.x =  self.SCREEN_X - 140 - 80 -  self.totfuel + (self.totfuel-params)

        world.blit( self.image , self.imagebox)
        world.blit( self.image , self.imagebox)

        world.blit( self.gaugeframe,self.gaugeframerect)
        if params > 0:
            world.blit( self.gauge,self.gaugerect)


r'''
      (\__/) 
      (•ㅅ•)      my support making ganks
   ＿ノ ヽ ノ＼__   and keeping me safe
 /　`/ ⌒Ｙ⌒ Ｙ　ヽ     
( 　(三ヽ人　 /　 |     
|　ﾉ⌒＼ ￣￣ヽ　 ノ    
ヽ＿＿＿＞､＿＿_／ 
　　 ｜( 王 ﾉ〈 (\__/) 
　　 /ﾐ`ー―彡\  (•ㅅ•)  me waiting to ruin the game
'''


class SpaceShip(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self,player_id):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.deadtimer = 0

        self.movex = 0
        self.movey = 0
        self.accelx = 0
        self.accely = 0
        self.drag = 0
        self.frame = 0
        self.angle = 0
        self.images = []
        self.deathanim = []
        self.chat = False
        self.baloon = Baloon()
        self.hud = Hud(player_id)
        self.shadow = Shadow()
        self.is_interacting = False
        self.speedx = 0
        self.speedy = 0
        self.ismoving= False
        self.speed = 10
        self.fuel = 300

        self.death_sfx = pygame.mixer.Sound(os.path.join(libpath,'res', 'player',"explosion_sfx.ogg"))
        self.death_sfx.set_volume(0.1)
        self.id = player_id

        for i in range(1, 3):
            img = pygame.image.load(os.path.join(libpath,'res', 'player','player'+str(player_id)+'_'+str(i)+'.png')).convert_alpha()
            img.convert_alpha()  # optimise alpha
            #img.set_colorkey(ALPHA)  # set alpha
            self.images.append(img)
            self.image = self.images[0]

        for i in range(1,9):
            img = pygame.image.load(os.path.join(libpath,'res', 'player','explosion-0'+str(i)+'.png')).convert_alpha()
            img.convert_alpha()  # optimise alpha
            img.set_colorkey(ALPHA)  # set alpha
            self.deathanim.append(img)
            self.image = self.images[0]

        boundingbox = pygame.transform.rotate(self.image,45)
        self.rect = boundingbox.get_rect()

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    # update according to boundaries
    def update(self,bound_to = None):
        """
        Update sprite position
        """
        
        if self.alive and self.fuel>0:

            self.rect.x = self.rect.x + self.movex
            if bound_to != None:
                if(self.rect.center[0]<0 or self.rect.center[0]>bound_to[0]):
                    self.rect.x = self.rect.x - 2*self.movex

            self.rect.y = self.rect.y + self.movey    
            if bound_to != None:
                if(self.rect.center[1]<0 or self.rect.center[1]>bound_to[1]):
                
                    self.rect.y = self.rect.y - 2*self.movey    
        
        if(self.chat):
            self.baloon.rect.x = self.rect.x+30
            self.baloon.rect.y = self.rect.y-30
        else:
            self.baloon.rect.x = -200
            self.baloon.rect.y = -200

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        self.update_shapes()

    # update according to collisions
    def update_2(self,collidelist):

        if self.alive:
            self.rect.y = self.rect.y + self.movey    
            self.rect.x = self.rect.x + self.movex

            if self.check_collision_simple(collidelist):
                self.rect.x = self.rect.x - 1.1*self.movex
                self.rect.y = self.rect.y - 1.1*self.movey    
        
        self.update_shapes()


 
    def update_shapes(self):

        if self.ismoving:
            self.fuel -= 1


        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        self.update_angle()

        if self.alive:
            self.image = pygame.transform.rotate(self.images[self.ismoving and (self.fuel>0)], self.angle)
    
        else:     
            self.image = self.deathanim[int(self.deadtimer)]
            if self.deadtimer<7:
                self.deadtimer +=0.1

    def update_angle(self):
        oldangle=0
        offset = 90
        self.ismoving = 0

        #update angle
        # moving left
        if self.movex < 0:
            self.ismoving = 1
            self.angle =offset
            if self.movey>0:
                self.angle = 45+offset
            if self.movey<0:
                self.angle = 315+offset

        # moving right
        if self.movex > 0:
            self.ismoving = 1            
            self.angle = 180+offset
            if self.movey>0:
                self.angle = 135+offset
            if self.movey<0:
                self.angle =225+offset

        if self.movex==0:           
            if self.movey>0:
                self.ismoving = 1
                self.angle = 90+offset
            if self.movey<0:
                self.ismoving = 1
                self.angle =270+offset



    def showchat(self,showval):
        if showval == 1:
            self.chat = True
        else:
            self.chat = False

    #callback function for interaction
    def interact(self,interaction_vector=None):
        
        if interaction_vector == None:
            self.is_interacting = True
            return

        if interaction_vector == False:
            self.is_interacting = False
            return
            
        for item in interaction_vector:

            x1 = item.rect.topleft
            x2 = item.rect.bottomright
            
            if self.rect.center[0] < x2[0] and self.rect.center[0] > x1[0] and self.rect.center[1] <x2[1] and self.rect.center[0]>x1[1]:
                #print("interacting with "+item)
                return item

    # very, veeeery, simple
    def check_collision_simple(self, interaction_vector):

        for (idx,item) in enumerate(interaction_vector):

            if self.rect.collidepoint(item.rect.center[0],item.rect.center[1]):
                return item
        
        return False

    def check_collision_list_fast(self, list_in):

        for item in list_in: 
            if self.rect.colliderect(item.rect) ==True:
                return True
            
        return False
    
    def die(self):
        self.death_sfx.play()
        self.alive = False
        pass

    def drawhud(self,world):
        self.hud.draw(world,self.fuel) 
        if self.chat:
            self.baloon.rect.x = self.rect.x+30
            self.baloon.rect.y = self.rect.y-30
            self.baloon.draw(world)


    def draw(self, world):
        if self.is_interacting:
            self.shadow.rect.center = self.rect.center
            self.shadow.draw(world)

        #probably slow BUT!
        world.blit(self.image,self.rect)

     