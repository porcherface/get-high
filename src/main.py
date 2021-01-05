#!/usr/bin/env python3
# LETS GO GET HIGH DEMO

# GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import sys
import os
import pathlib
import game.lib.manager as libm
import argparse
import ctypes

from pygame.locals import FULLSCREEN as FULLSCREEN

mainpath = pathlib.Path(__file__).parent.absolute()

# two global variable passed as arguments
# THESE TWO ARE THE ONLY ALLOWED TO PROPAGATE!
MY_AUDIO_IS_WORKING = True
DEBUG_MODE = False

'''
arg parse
'''
parser = argparse.ArgumentParser()
parser.add_argument("-n","--noaudio", help="turn off audio cus my pc is pussy",action="store_true")
parser.add_argument("-d","--debug", help="skip to level under work on launch",action="store_true")
parser.add_argument("-w","--windows",help="i got windows",action="store_true")

args = parser.parse_args()

if args.windows:
    os.add_dll_directory(os.path.join(mainpath,"dll"))
if args.noaudio:
    MY_AUDIO_IS_WORKING = False
if args.debug:
    DEBUG_MODE = True

libm.get_globals(DEBUG_MODE,MY_AUDIO_IS_WORKING)

'''
INIT
'''
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
if MY_AUDIO_IS_WORKING:
    pygame.mixer.init()
else:
    print("pussy")
    sys.exit(1)
# uncomment these lines to go fullscreen mode
#infoObject = pygame.display.Info()
#pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

# uncomment these lines to go custom resolution mode
#infoObject = pygame.display.Info()
#pygame.display.set_mode((1600, 900),FULLSCREEN)


'''
Setup
'''
programIconPath = os.path.join(mainpath,'game','lib','res', 'player','player2_2.png')
print("gettin paths from: "+programIconPath)
programIcon = pygame.image.load(programIconPath)
pygame.display.set_icon(programIcon)
libm.SceneManager()


# THE GAME
if __name__ == "__main__":

    pass
