#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Last Updated: 2015-03-13
#
# This tutorial is intended as a initial panda scripting lesson going over
# display initialization, loading models, placing objects, and the scene graph.
#
# Step 1: ShowBase contains the main Panda3D modules. Importing it
# initializes Panda and creates the window. The run() command causes the
# real-time simulation to begin

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode, NodePath, LightAttrib
from panda3d.core import LVector3
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import sys
from direct.interval.IntervalGlobal import *

# base = ShowBase()
from direct.gui.DirectGui import *
from panda3d.core import Point3



class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        # This code puts the standard title and instruction text on screen
        # format borrowed
        self.title = OnscreenText(text="Try 2 at fish tanks",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)

        # Set up key input, borrowed
        self.accept('escape', sys.exit)


        # base.disableMouse()  # Disable mouse-based camera-control
        # camera.setPos(-2, -10, 1)  # -x, -z, -y Position the camera
        # camera.setHpr(0, 0, 0)
        base.trackball.node().setPos(0, 30, -1) # starting position of the camera
        self.fishR = Actor("models/fish1bend-1")  # Load our animated charachter
        
        # syntax for loading the fish from Panda3d website
        fishTex = loader.loadTexture('tex/TropicalFish01.jpg')
        self.fishR.setTexture(fishTex)
        self.fishR.reparentTo(render)
        # set a starting position for the right tail fish
        self.fishR.setPos((0, -1, 0))

        # create alternate fish the left tail position (from fish perspective)
        self.fishL = Actor("models/fish1bend2-1")  # Load our animated charachter
        self.fishL.setTexture(fishTex)
        self.fishL.reparentTo(render)
        
        self.fishFront = Actor("models/fish1front_04")
        self.fishFront.setTexture(fishTex) # use same previous fishTex
        self.fishFront.reparentTo(render)
        
        # start with just one model
        self.fishR.hide()
        self.fishFront.hide()

        # initialize how far the fish moves each time
        self.distanceMoved = -1
        # moving one fish and its tial
        self.moveTail()

    def moveTailLeft(self):
        # increment the distance of the fish
        self.distanceMoved -= 1
        if self.distanceMoved == -20: self.distanceMoved = 0
        self.fishR.hide()
        self.fishFront.hide()
        # fish is moving self.distanceMoved space
        self.fishL.setPos((0, self.distanceMoved, 0))
        self.fishL.show()

    def moveTailRight(self):
        self.distanceMoved -= 1
        if self.distanceMoved == -20: self.distanceMoved = 0
        self.fishL.hide()
        self.fishFront.hide()
        self.fishR.setPos((0, self.distanceMoved, 0))
        self.fishR.show()

    def moveTailCenter(self):
        self.distanceMoved -= 1
        if self.distanceMoved == -20: self.distanceMoved = 0
        self.fishL.hide()
        self.fishR.hide()
        self.fishFront.setPos((0, self.distanceMoved, 0))
        self.fishFront.show()

    def moveTail(self):
        seq = Sequence() # syntax for Sequence from Panda3D library and forums
        seq.append(Wait(.25))
        seq.append(Func(self.moveTailRight))
        seq.append(Wait(.25))
        seq.append(Func(self.moveTailCenter))
        seq.append(Wait(.25))
        seq.append(Func(self.moveTailLeft))
        seq.append(Wait(.25))
        seq.append(Func(self.moveTailCenter))
        seq.loop()





# w = World()
# base.run()

# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
demo = fishTank()  # Create an instance of our class
demo.run()  # Run the simulation


