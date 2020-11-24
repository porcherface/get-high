#!/usr/bin/env python3
import pathlib
import os

rootpath = pathlib.Path(__file__).parents[1]

libpath =  os.path.join(rootpath,"src","game","lib","res")
playerpath =  os.path.join(libpath,"player")
buttonspath = os.path.join(libpath,"buttons")
enemypath = os.path.join(libpath,"enemy")

print(libpath)
print(playerpath)
print(buttonspath)
print(enemypath)
