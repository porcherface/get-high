#!/usr/bin/env python3
import os
import pygame 

import game.scenes.title.title as title
import game.scenes.asteroids.asteroids as asteroids
import game.scenes.landing.landing as landing
import game.scenes.launchvid.launchvid as launchvid
import game.scenes.labyrinth.labyrinth as labyrinth
import game.scenes.spring.spring as spring

def get_globals(debug,goodaudio):
    global DEBUG_MODE
    DEBUG_MODE = debug
    global MY_AUDIO_IS_WORKING
    MY_AUDIO_IS_WORKING = goodaudio

class SceneManager(object):
    def __init__(self): 

        # global variables still propagating
        # VERY VERY BAD
        launchvid.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)
        title.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)
        asteroids.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)
        landing.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)
        labyrinth.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)
        spring.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)

        ###############
        # debug miniloop
        if DEBUG_MODE:
            a_little_loop=True
            while a_little_loop : 
                scene = landing.LandingScene()
                #scene = labyrinth.LabyrinthScene()
                #scene = spring.SpringScene()
                #a_little_loop = False
                #asteroids.AsteroidScene()
            return

        ##############################################
        ##############################################
        ##########     GAME STATES HERE      #########
        ##############################################
        ##############################################    
        scene = launchvid.LaunchvidScene()
        scene = title.TitleScene()
        #print(scene)
        GAME_LOOP = True
        while GAME_LOOP:
            if(scene.STATE == 0): 
                # start journey # a story mode?
                print("came here from start journey, TBD")
                # as for now, this scene is a guaranteed death, always returns 0
                scene = asteroids.AsteroidScene()
                scene = landing.LandingScene()
                scene = labyrinth.LabyrinthScene()
                #scene = spring.SpringScene()
                return 
            if(scene.STATE == 1):
                print("no loadlevel gui yet, bye!xoxoxo")                
        # GAME LOOP/STORY FINISHED
        return 
            
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
