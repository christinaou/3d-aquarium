# Christina Ou
# AndrewID: cou
# term project
# previous files and versions are in backups folder
# Used Panda3D and Blender
# Blender to create the models which are borrowed from turbosquid
#   and to position the models to simulate moving

# Using Panda3D's libraries to enact the 3D model of my aquarium

# Aquarium

# Panda imports to enable what I'm doing
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, NodePath, LightAttrib
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
import sys
from direct.interval.IntervalGlobal import *

import random

# FYI: some of the uncommented code is for my own testing purposes


class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        base.setBackgroundColor(0, 0, 0) # set background black
        # This code puts the standard title and instruction text on screen
        # format borrowed
        self.title = OnscreenText(text="",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)

        # Set up key input, borrowed
        self.accept('escape', sys.exit)

        # set initial camera position
        # base.disableMouse()  # Disable mouse-based camera-control
        # x, y, z is actually i, k, j Position the camera
        base.trackball.node().setPos(0, 150, -20) # starting position of camera
        base.trackball.node().setHpr(0,0,0)

        # positioning is x, -y, z, where x is i, -y is k, z is j
        self.marker = self.loader.loadModel("models/marker_01")
        self.marker.reparentTo(self.render)
        self.marker.setPos(0, 0, 30)

        # positioning is x, -y, z, where x is i, -y is k, z is j
        self.marker3 = self.loader.loadModel("models/marker_01")
        self.marker3.reparentTo(self.render)
        self.marker3.setPos(0, 0, 0)

        self.wood = self.loader.loadModel("models/wood_0")
        woodTex = loader.loadTexture("tex/L1.jpg")
        self.wood.setTexture(woodTex)
        self.wood.reparentTo(self.render)
        self.wood.setScale(20,20,20)
        self.wood.setPos(5, 2, 0)

        # call method to create tank model
        self.createTank()
        # get the dimensions (scale, width, height, length of present tank)
        tankDims = self.getTankDims()

        # keep track of all the fish
        self.fishList = []
        # types of fish; there are 4 right now

        # fish1 contains models of fish rightbend, leftbend, and centered
        # also stores the image jpg of the fish for its texture
        fish1 = ["models/fish1bend-1", "models/fish1bend2-1", 
        "models/fish1front_04", 'tex/TropicalFish01.jpg']
        # pos1 = (-22, 35, 30)
        pos1 = (0, 0, 15)
        self.fishOne = Fish(fish1, pos1, tankDims) # instantiated in fish class

        # repeat for a total of 4 fish
        fish2 = ["models/tang_right_00", "models/tang_left_01", 
        "models/tang_02", "tex/TropicalFish02.jpg"]
        # pos2 = (22, 35, 30)
        pos2 = (0, 0, 15)
        self.fishTwo = Fish(fish2, pos2, tankDims)
        # 22 35 30 is where top left forward corner is

        fish3 = ["models/nemo_right_2", "models/nemo_left_2", 
        "models/nemo_front_2", "tex/TropicalFish12.jpg"]
        # pos3 = (0, 0, 4)
        pos3 = (0, 0, 15)
        self.fishThree = Fish(fish3, pos3, tankDims)

        fish4 = ["models/yellow_right_0", "models/yellow_left_0", 
        "models/yellow_front_0", "tex/TropicalFish05.jpg"]
        # pos4 = (22, -35, 30)
        pos4 = (0, 0, 15)
        self.fishFour = Fish(fish4, pos4, tankDims)

        self.fishList = ([self.fishOne] + [self.fishTwo] + 
        [self.fishThree] + [self.fishFour])

        # move/run the movement
        for fish in self.fishList:
            fish.move()
        # self.fishThree.move()
        # self.fishTwo.move()
        # self.fishOne.move()


    def createTank(self):
        # loader.loadModel borrowed from Panda3D's first program example
        # models from Blender
        self.sides = self.loader.loadModel("models/tanksides_03")
        # set texture from image
        sidesTex = loader.loadTexture("tex/blue.png")
        self.sides.setTexture(sidesTex)
        # attach the model to render so it appears in window
        self.sides.reparentTo(self.render)

        self.tankLength, self.tankWidth, self.tankHeight = 3, 2, 2
        self.tankScale = 15

        # Apply scale and position transforms on the model.
        # make the model 15x larger
        self.sides.setScale(self.tankScale, self.tankScale, self.tankScale)
        self.sides.setPos(0, 0, 0) # set the position

        # do same for bottom of tank, bottom is sand color 
        self.bottom = self.loader.loadModel("models/tankbott_05")
        bottomTex = loader.loadTexture("tex/sand.jpg")
        self.bottom.setTexture(bottomTex)
        self.bottom.reparentTo(self.render)
        self.bottom.setScale(self.tankScale, self.tankScale, self.tankScale)
        self.bottom.setPos(0,0,0)

    def getTankDims(self):
        return self.tankScale, self.tankLength, self.tankWidth, self.tankHeight

# fish class for each instance of the fish
# need to specify what type, which position
# everythingFish contains all the methods necessary for a Fish
# contains more than 1 fish needs, so it's the superclass of Fish
class EverythingFish(fishTank):

    def __init__(self, fishModel, position, tankDims):
        # I have 3 fish models for each one instance.
        # This is due to me creating an animation out of frames of the fish
        # To make them "move", I have a fish with 3 positions: tail straight,
        # tail bending right, and tail bending left

        # use loader to load the model of the fish
        # don't need panda's "actors" because I'm not utilizig Blender's
        # animation technique
        self.fishR = loader.loadModel(fishModel[0])
        # syntax for loading the fish from Panda3d website
        fishTex = loader.loadTexture(fishModel[3])
        self.fishR.setTexture(fishTex)
        self.fishR.reparentTo(render)

        # create alternate fish the left tail position (from fish perspective)
        self.fishL = loader.loadModel(fishModel[1])
        self.fishL.setTexture(fishTex)
        self.fishL.reparentTo(render)
        
        self.fishFront = loader.loadModel(fishModel[2])
        self.fishFront.setTexture(fishTex) # use same previous fishTex
        self.fishFront.reparentTo(render)

        # start with just one model
        self.fishR.hide()
        self.fishFront.hide()

        # initialize how far the fish moves each time
        self.xPosition = position[0]
        self.yPosition = position[1]
        self.zPosition = position[2]

        self.fishL.setPos((self.xPosition, self.yPosition, self.zPosition))
        # starting fish image set to the positions

        # initialize initial direction
        # change will see which direction the fish is going next time
        self.yChange = -1 # start by going forward
        self.xChange = 0
        self.zChange = 0

        # initialize pitch and heading move each time the fish turns
        self.pitchChange = 0
        self.headingChange = 0

        # set a variable so not turning every sequence call
        self.fishTurn = 0

        self.tankScale, self.tankLength, self.tankWidth, self.tankHeight = tankDims
        self.hitBound = False

    # every time I move the tail, I also move the fish. I take in how much the 
    # z and x are changing and  increment the positions of the fish's z and x

    # When I "move" the fish, I am essentially looking at a different snapshot 
    # of the fish that is set to a new position so it gives the illusion of 
    # "moving forward". To accomplish this, I need to hide the other images 
    # of the fish, and set the new fish's position to the "moving forward" one
    # Then I show that fish, and it has moved forward. Voila!
    def moveTailLeft(self):
        # increment the distance of the fish
        self.checkBounds()
        self.yPosition += self.yChange
        self.xPosition += self.xChange
        self.zPosition += self.zChange

        self.fishR.hide()
        self.fishFront.hide()
        # fish is moving in x,z,y space
        self.fishL.setPos((self.xPosition, self.yPosition, self.zPosition))
        self.fishL.show()

    def moveTailRight(self):
        self.checkBounds()
        self.yPosition += self.yChange
        self.xPosition += self.xChange
        self.zPosition += self.zChange

        self.fishL.hide()
        self.fishFront.hide()
        self.fishR.setPos((self.xPosition, self.yPosition, self.zPosition))
        self.fishR.show()

    def moveTailCenter(self):
        self.checkBounds()
        self.yPosition += self.yChange
        self.xPosition += self.xChange
        self.zPosition += self.zChange
  
        self.fishL.hide()
        self.fishR.hide()
        self.fishFront.setPos((self.xPosition, self.yPosition, self.zPosition))
        self.fishFront.show()

    # turning the fish 45 degrees each time. need to make sure to change
    # how much x and z changes according to the direction the fish is facing
    def leftRightFish(self, numm):
        self.fishTurn += 1
        # self.fishTurn sets how far the fish moves before turning
        if self.fishTurn < 3: 
            return
        else:
            self.fishTurn = 0
        # random which direction
        if numm == 0:
            self.pitchChange = (self.pitchChange+45)%360 # turn left
        elif numm == 1:
            self.pitchChange = (360 + self.pitchChange - 45)%360 # turn right
        # coordinate changes for which way the fish is facing
        # Using the x and z axis
        if self.pitchChange == 0:
            self.xChange, self.yChange = 0, -1
        elif self.pitchChange == 45:
            self.xChange, self.yChange = +1, -1
        elif self.pitchChange == 90:
            self.xChange, self.yChange = +1, 0
        elif self.pitchChange == 135:
            self.xChange, self.yChange = +1, +1
        elif self.pitchChange == 180:
            self.xChange, self.yChange = 0, +1
        elif self.pitchChange == 225:
            self.xChange, self.yChange = -1, +1
        elif self.pitchChange == 270:
            self.xChange, self.yChange = -1, 0
        elif self.pitchChange == 315:
            self.xChange, self.yChange = -1, -1
        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    # appends these movements for a moveStraight movement
    # eventually also create a turn method that modifies/adds on to the 
    # sequence
    # This is the crux of moving the fish. Credits to Panda3D library for 
    # helping me figure out how to loop through functions through its Sequence
    # method. In this sequence, I loop through moving the tail from center to
    # left back to center to right. Then I turn the fish. In between each, I 
    # have the program wait for a period of time so that we can see each frame.
    def moveStraight(self, seq):
        seq.append(Wait(.15))
        seq.append(Func(self.moveTailCenter))
        seq.append(Wait(.15))
        seq.append(Func(self.moveTailLeft))
        seq.append(Wait(.15))
        seq.append(Func(self.moveTailCenter))
        seq.append(Wait(.15))
        seq.append(Func(self.moveTailRight))

    # move fish up or down
    # includes pointing nose of fish up or down, then "y" axis shift
    def upDownFish(self, numm):
        # restrict to 30 degree angle
        if numm == 0 and self.headingChange > -30: # moving up
            self.headingChange -= 30 # angle fish pointing up
            self.zChange += 1

        elif numm == 1 and self.headingChange < 30: # moving down
            self.headingChange += 30
            self.zChange -= 1

        else:
            self.headingChange = 0
            self.zChange = 0

        # set the new rotation for each of the models
        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    def checkBounds(self):
        zLimit = self.tankHeight*self.tankScale
        xLimit = self.tankScale*self.tankLength
        yLimit = self.tankScale*self.tankWidth
        zmargin = 5
        xymargin = 10
        # print(self.xPosition, self.yPosition, self.zPosition)
        if self.zPosition < zmargin - 1: # actual basically bottom is 4
            # print("z low")
            self.upDownFish(0) # make fish move up
            return True
        if self.zPosition > zLimit - zmargin: # actual basically top is 30
            # print("z high")
            self.upDownFish(1)
            return True

        if self.xPosition > xLimit - xymargin:
            if self.pitchChange < 90:
                self.leftRightFish(1)
            else: self.leftRightFish(0)
            return True

        if self.yPosition > yLimit - xymargin:
            # print("y high")
            if self.pitchChange >= 180 or self.pitchChange == 0:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
            return True

        if self.xPosition < -xLimit + xymargin:
            # print("x low")
            if self.pitchChange < 270 and self.pitchChange != 0:
                self.leftRightFish(1)
            else: 
                self.leftRightFish(0)
            return True

        if self.yPosition < -yLimit + zmargin:
            # print("y low")
            if self.pitchChange < 180:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
            return True
        return False

    def UDLRFish(self):
        if self.checkBounds() != True:
            numm = random.randint(0,2) # turnLR or UD 2/3 of the time
            if numm == 1 or numm == 2: # random L or R turn
                leftrightNum = random.randint(0,1)
                self.leftRightFish(leftrightNum)
            # otherwise move up or down
            elif numm == 0: # random U or D motion
                updownNum = random.randint(0, 1)
                self.upDownFish(updownNum)



class Fish(EverythingFish):

    def __init__(self, fishModel, position, tankDims):
        EverythingFish.__init__(self, fishModel, position, tankDims)

    # create a sequence, a loop of functions. call the superclasses' methods
    # to add to the sequence of these fish
    def move(self):
        seq = Sequence()
        self.moveStraight(seq)
        seq.append(Func(self.UDLRFish))
        seq.loop()





# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
tank = fishTank()  # Create an instance of our class
tank.run()  # Run the simulation


