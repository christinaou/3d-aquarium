# Christina Ou
# AndrewID: cou
# term project
# previous files and versions are in backups folder
# Used Panda3D and Blender
# Blender to create the models which are borrowed from turbosquid
#   and to position the models to simulate moving

# Using Panda3D's libraries to enact the 3D model of my aquarium

# Aquarium


from direct.showbase.ShowBase import ShowBase
# from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode, NodePath, LightAttrib
# from panda3d.core import LVector3
from direct.actor.Actor import Actor
# from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
# from direct.showbase.DirectObject import DirectObject
import sys
from direct.interval.IntervalGlobal import *

# from direct.gui.DirectGui import *
# from panda3d.core import Point3
import random


class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        # base.setBackgroundColor(0, 0, 0) # set background black
        # This code puts the standard title and instruction text on screen
        # format borrowed
        self.title = OnscreenText(text="I <3 Fish",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)

        # Set up key input, borrowed
        self.accept('escape', sys.exit)

        # set initial camera position
        # base.disableMouse()  # Disable mouse-based camera-control
        # camera.setPos(-2, -10, 1)  # -x, -z, -y Position the camera
        # camera.setHpr(0, 0, 0)
        base.trackball.node().setPos(0, 180, -25) # starting position of the camera
        base.trackball.node().setHpr(-90,0,0)


        # borrowed from Panda3D's first program example
        self.sides = self.loader.loadModel("models/tanksides_01")
        # set texture
        sidesTex = loader.loadTexture("tex/blue.png")
        self.sides.setTexture(sidesTex)
        # Reparent the model to render.
        self.sides.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.sides.setScale(15, 15, 15)
        self.sides.setPos(0, 0, 0)

        self.bottom = self.loader.loadModel("models/tankbott_02")
        bottomTex = loader.loadTexture("tex/brown.jpg")
        self.bottom.setTexture(bottomTex)
        self.bottom.reparentTo(self.render)
        self.bottom.setScale(15,15,15)
        self.bottom.setPos(0,0,0)

        self.fishList = []

        # types of fish; there are 4 right now
        # images of fish rightbend, leftbend, and front
        fish1 = ["models/fish1bend-1", "models/fish1bend2-1", 
        "models/fish1front_04", 'tex/TropicalFish01.jpg']
        pos1 = (-22, 35, 30)
        self.fishOne = Fish(fish1, pos1)

        fish2 = ["models/tang_right_00", "models/tang_left_01", 
        "models/tang_02", "tex/TropicalFish02.jpg"]
        pos2 = (22, 35, 30)
        self.fishTwo = Fish(fish2, pos2)
        # 22 35 30 is where top left forward corner is

        fish3 = ["models/nemo_right_2", "models/nemo_left_2", 
        "models/nemo_front_2", "tex/TropicalFish12.jpg"]
        pos3 = (0, 0, 4)
        self.fishThree = Fish(fish3, pos3)

        fish4 = ["models/yellow_right_0", "models/yellow_left_0", 
        "models/yellow_front_0", "tex/TropicalFish05.jpg"]
        pos4 = (22, -35, 30)
        self.fishFour = Fish(fish4, pos4)

        self.fishList += [self.fishOne] + [self.fishTwo] + [self.fishThree] + [self.fishFour]

        # for fish in self.fishList:
        #     fish.move()
        # self.fishThree.move()
        # self.fishTwo.move()
        # self.fishOne.move()


# fish class for each instance of the fish
# need to specify what type, which position, and movement type
class EverythingFish(object):

    def __init__(self, fishModel, position):
        # I have 3 fish models for each one instance.
        # This is due to me creating an animation out of frames of the fish
        # To make them "move", I have a fish with 3 positions: tail straight,
        # tail bending right, and tail bending left

        self.fishR = Actor(fishModel[0])  # Load our animated character
        
        # syntax for loading the fish from Panda3d website
        fishTex = loader.loadTexture(fishModel[3])
        self.fishR.setTexture(fishTex)
        self.fishR.reparentTo(render)

        # set a starting position for the right tail fish

        # create alternate fish the left tail position (from fish perspective)
        self.fishL = Actor(fishModel[1])  # Load our animated charachter
        self.fishL.setTexture(fishTex)
        self.fishL.reparentTo(render)
        
        self.fishFront = Actor(fishModel[2])
        self.fishFront.setTexture(fishTex) # use same previous fishTex
        self.fishFront.reparentTo(render)

        # set limits for where the fish can travel
        self.xLimits = (-20, 20)
        self.yLimits = (-20, 20)
        self.zLimits = (-10, 20)

        # start with just one model
        self.fishR.hide()
        self.fishFront.hide()

        # initialize how far the fish moves each time
        self.xPosition = position[0]
        self.zPosition = position[1]
        self.yPosition = position[2]

        self.fishL.setPos((self.xPosition, self.zPosition, self.yPosition))

        # initialize initial direction
        # change will see which direction the fish is going next time
        self.zChange = -1
        self.xChange = 0
        self.yChange = 0

        # initialize pitch move each time the fish turns
        self.pitchChange = 0
        self.headingChange = 0

        # set a variable so not turning every sequence call
        self.fishTurn = 0


    # every time I move the tail, I also move the fish. I take in how much the 
    # z and x are changing and thus increment the positions of the fish's z and x

    # When I "move" the fish, I am essentially looking at a different snapshot 
    # of the fish that is set to a new position so it gives the illusion of 
    # "moving forward". To accomplish this, I need to hide the other images 
    # of the fish, and set the new fish's position to the "moving forward" one
    # Then I show that fish, and it has moved forward. Voila!
    def moveTailLeft(self):
        # increment the distance of the fish
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        self.yPosition += self.yChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0
        self.fishR.hide()
        self.fishFront.hide()
        # fish is moving self.zPosition space
        self.fishL.setPos((self.xPosition, self.zPosition, self.yPosition))
        self.fishL.show()

    def moveTailRight(self):
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        self.yPosition += self.yChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0
        self.fishL.hide()
        self.fishFront.hide()
        self.fishR.setPos((self.xPosition, self.zPosition, self.yPosition))
        self.fishR.show()

    def moveTailCenter(self):
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        self.yPosition += self.yChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0        
        self.fishL.hide()
        self.fishR.hide()
        self.fishFront.setPos((self.xPosition, self.zPosition, self.yPosition))
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
            self.xChange, self.zChange = 0, -1
        elif self.pitchChange == 45:
            self.xChange, self.zChange = +1, -1
        elif self.pitchChange == 90:
            self.xChange, self.zChange = +1, 0
        elif self.pitchChange == 135:
            self.xChange, self.zChange = +1, +1
        elif self.pitchChange == 180:
            self.xChange, self.zChange = 0, +1
        elif self.pitchChange == 225:
            self.xChange, self.zChange = -1, +1
        elif self.pitchChange == 270:
            self.xChange, self.zChange = -1, 0
        elif self.pitchChange == 315:
            self.xChange, self.zChange = -1, -1
        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    # appends these movements for a moveStraight movement
    # eventually also create a turn method that modifies/adds on to the 
    # sequence
    # This is the crux of moving the fish. Credits to Panda3D library for helping
    # me figure out how to loop through functions through its Sequence method.
    # In this sequence, I loop through moving the tail from center to left back
    # to center to right. Then I turn the fish. In between each, I have the program
    # wait for a period of time so that we can see each frame.
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
            self.yChange += 1

        elif numm == 1 and self.headingChange < 30: # moving down
            self.headingChange += 30
            self.yChange -= 1

        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    def UDLRFish(self):
        numm = random.randint(0,2) # turnLR or UD 2/3 of the time
        if numm == 1 or numm == 2: # random L or R turn
            leftrightNum = random.randint(0,1)
            self.leftRightFish(leftrightNum)
        # otherwise move up or down
        elif numm == 0: # random U or D motion
            updownNum = random.randint(0, 1)
            self.upDownFish(updownNum)



class Fish(EverythingFish):

    def __init__(self, fishModel, position):
        EverythingFish.__init__(self, fishModel, position)

    def move(self):

        seq = Sequence()
        self.moveStraight(seq)
        seq.append(Func(self.UDLRFish))
        seq.loop()





# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
demo = fishTank()  # Create an instance of our class
demo.run()  # Run the simulation


