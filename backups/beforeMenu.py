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
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor



# for Panda3D's DirectGUI
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *

import sys
from direct.interval.IntervalGlobal import *
from panda3d.core import Fog


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
        self.title = OnscreenText(text="Sea World",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)

        # GUI things
        tangObject = OnscreenImage(image = 'fishPics/blueTang.png', 
            pos = (-1, 0, -.5), scale = 0.23)
        sailfinObject = OnscreenImage(image = 'fishPics/sailfinTang.png', 
            pos = (-.5, 0, -.5), scale = 0.2)
        yellowObject = OnscreenImage(image = 'fishPics/yellowTang.png', 
            pos = (0, 0, -.5), scale = 0.2)
        nemoObject = OnscreenImage(image = 'fishPics/clownFish.png', 
            pos = (.5, 0, -.5), scale = 0.2)


        # Set up key input, borrowed
        self.accept('escape', sys.exit)
        
        # set initial camera position
        # base.disableMouse()  # Disable mouse-based camera-control
        # x, y, z is actually i, k, j Position the camera
        base.trackball.node().setPos(0, 170,0) # starting position of camera
        base.trackball.node().setHpr(0,20,0)

        # call method to create tank model
        self.createTank()
        # get the dimensions (scale, width, height, length of present tank)
        self.tankDims = self.getTankDims()
        self.fishList = []
        self.GUI()

    def setFish(self, fishType):
        self.currentFish = fishType
        if fishType == "blue tang":
            x, textt = -1, "Blue Tang"
            # self.bTButt = DirectButton(text = ("Blue Tang"),
            # scale = 0.08, pos = (x,0,-.8), frameColor = (0,100,50,.5))
        if fishType == "sailfin tang":
            x, textt = -.5, "Sailfin Tang"
            # self.bTButt = DirectButton(text = ("Sailfin Tang"),
            # scale = 0.08, pos = (x,0,-.8), frameColor = (0,100,50,.5))
        if fishType == "yellow tang":
            x, textt = 0, "Yellow Tang"
            # self.bTButt = DirectButton(text = ("Yellow Tang"),
            # scale = 0.08, pos = (x,0,-.8), frameColor = (0,100,50,.5))
        if fishType == "clown fish":
            x, textt = .5, "Clown Fish"
            # self.bTButt = DirectButton(text = ("Clown Fish"),
            # scale = 0.08, pos = (x,0,-.8), frameColor = (0,100,50,.5))
        self.newButt = DirectButton(text = (textt), scale = 0.08, pos = 
            (x,0,-.8), frameColor = (0,100,50,.5))
        self.addButt = DirectButton(text = ("Add", "", "Add?", "disabled"),
            scale = 0.08, command = self.addFish, pos = (x,0,-.9))

    def addFish(self):
        self.fishList += [Fish(self.currentFish, self.tankDims)]

    # borrowed syntax for isPlaying and pause
    def stop(self):
        print("stop")
        self.playButt = DirectButton(text = ("Run", "", "Run?", "disabled"), 
            scale = 0.08, command = self.moveFish, pos = (+1, 0, -.8))
        for fish in self.fishList:
            if fish.seq.isPlaying():
                fish.seq.pause()

    def moveFish(self):
        print("moving")
        self.playButt = DirectButton(text = ("Run"), scale = 0.08, 
            pos = (+1, 0, -.8), command = self.stop, frameColor = (0,100,50,1))
        for fish in self.fishList:
            try: # if paused
                fish.seq.loop()
            except: # start the sequence and movement
                fish.move()

    # DirectGUI interface from Panda3D. Looked at its syntax for DirectButtons
    def GUI(self):
        # GUI outside the classes, so can happen any time
        self.bTButt = DirectButton(text = ("Blue Tang"),
            scale = 0.08, command = self.setFish, extraArgs = ["blue tang"], 
            pos = (-1,0,-.8))
        self.sFButt = DirectButton(text =("Sailfin Tang"),
            scale = 0.08, command = self.setFish, extraArgs = ["sailfin tang"],
             pos = (-.5,0,-.8))
        self.yTButt = DirectButton(text =("Yellow Tang"),
            scale = 0.08, command = self.setFish, extraArgs = ["yellow tang"],
            pos = (0,0,-.8))
        self.cFButt = DirectButton(text =("Clown Fish"),
            scale = 0.08, command = self.setFish, extraArgs = ["clown fish"], 
            pos = (+.5,0,-.8))

        self.playButt = DirectButton(text = ("Run", "", "Run?", "disabled"), 
            scale = 0.08, command = self.moveFish, pos = (+1, 0, -.8))



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

        # create wood decoration
        # borrowed wood model and texture
        # self.wood = self.loader.loadModel("models/wood_0")
        # woodTex = loader.loadTexture("tex/L1.jpg")
        # self.wood.setTexture(woodTex)
        # self.wood.reparentTo(self.render)
        # self.wood.setScale(20,20,20)
        # self.wood.setPos(11, -3, 0)
        # self.wood.setHpr(30,0,0)

        # borrowed bush model and texture
        self.bush = self.loader.loadModel("models/bush_0")
        bushTex = loader.loadTexture("tex/forestGreen.png")
        self.bush.setTexture(bushTex)
        self.bush.reparentTo(self.render)
        self.bush.setScale(20,20,20)
        self.bush.setPos(15,-8,0)

        # borrowed rock model and texture
        self.rock = self.loader.loadModel("models/rock_0")
        rockTex = loader.loadTexture("tex/rock.jpg")
        self.rock.setTexture(rockTex)
        self.rock.reparentTo(self.render)
        self.rock.setScale(20,20,20)
        self.rock.setPos(-20,5,0) 
        self.rock.setHpr(50,0,0)       


        # creating fog. borrowed from Panda3D's infinite-tunnel demo/tutorial
        # beg citation [
        # Create an instance of fog called 'distanceFog'.
        # 'distanceFog' is just a name for our fog, not a specific type of fog.
        self.fog = Fog('distanceFog')
        color = (.13, .204, .565)
        # Set the initial color of our fog to black.
        self.fog.setColor(*color)
        # Set the density/falloff of the fog.  The range is 0-1.
        # The higher the numer, the "bigger" the fog effect.
        self.fog.setLinearRange(-40,40)
        render.attachNewNode(self.fog)
        render.setFog(self.fog)
        # We will set fog on render which means that everything in our scene will
        # be affected by fog. Alternatively, you could only set fog on a specific
        # object/node and only it and the nodes below it would be affected by
        # the fog.
        # ] end citation

    def getTankDims(self):
        return self.tankScale, self.tankLength, self.tankWidth, self.tankHeight

# fish class for each instance of the fish
# need to specify what type, which position
# everythingFish contains all the methods necessary for a Fish
# contains more than 1 fish needs, so it's the superclass of Fish
class EverythingFish(fishTank):

    def __init__(self, typeFish, tankDims):
        self.tankScale, self.tankLength, self.tankWidth, self.tankHeight = tankDims

        fishModel = self.createFish(typeFish)
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
        self.fishR.setScale(1.5,1.5,1.5)

        # create alternate fish the left tail position (from fish perspective)
        self.fishL = loader.loadModel(fishModel[1])
        self.fishL.setTexture(fishTex)
        self.fishL.reparentTo(render)
        self.fishL.setScale(1.5,1.5,1.5)
        
        self.fishFront = loader.loadModel(fishModel[2])
        self.fishFront.setTexture(fishTex) # use same previous fishTex
        self.fishFront.reparentTo(render)
        self.fishFront.setScale(1.5,1.5,1.5)

        self.isMoving = False
        self.beginning()

    def beginning(self):
        # start with just one model
        self.fishR.hide()
        self.fishFront.hide()

        # initialize how far the fish moves each time
        self.xPosition = random.randint(-30,30)
        self.yPosition = random.randint(-20,20)
        self.zPosition = random.randint(0,30)
        self.fishL.setPos((self.xPosition, self.yPosition, self.zPosition))
        # starting fish image set to the positions

        # set a variable so not turning every sequence call
        self.fishTurn = 0

        self.hitBound = False

        # initialize pointing in random directions (pitch and heading)
        LRDir = [0,45,90,135,180,225,270,315]
        self.pitchChange = random.choice(LRDir)
        self.headingChange = random.choice([-30,0,30])
        self.fishL.setHpr(self.pitchChange, self.headingChange, 0)
        self.fishR.setHpr(self.pitchChange, self.headingChange, 0)
        self.fishFront.setHpr(self.pitchChange, self.headingChange, 0)

        # initialize initial direction. Setting xChange, yChange, and zChange
        self.findXYChange()
        if self.headingChange == -30: self.zChange = +1
        elif self.headingChange == 0: self.zChange = 0
        else: self.zChange = -1




    def createFish(self, fishType):
        # types of fish; there are 4 right now

        # fish1 contains models of fish rightbend, leftbend, and centered
        # also stores the image jpg of the fish for its texture

        fish1 = ["models/fish1bend-1", "models/fish1bend2-1", 
        "models/fish1front_04", 'tex/TropicalFish01.jpg']

        fish2 = ["models/tang_right_00", "models/tang_left_01", 
        "models/tang_02", "tex/TropicalFish02.jpg"]

        fish3 = ["models/nemo_right_2", "models/nemo_left_2", 
        "models/nemo_front_2", "tex/TropicalFish12.jpg"]

        fish4 = ["models/yellow_right_0", "models/yellow_left_0", 
        "models/yellow_front_0", "tex/TropicalFish05.jpg"]

        if fishType == "blue tang":
            return fish2
        elif fishType == "yellow tang":
            return fish4
        elif fishType == "clown fish":
            return fish3
        elif fishType == "sailfin tang":
            return fish1


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


    def findXYChange(self):
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
        # find change in x and y due to new pitch
        self.findXYChange()
        # coordinate changes for which way the fish is facing
        # Using the x and z axis

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
    def moveStraight(self):
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailCenter))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailLeft))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailCenter))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailRight))

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
        zmargin, xymargin = 5, 10
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

        if self.xPosition < -xLimit + xymargin:
            # print("x low")
            if self.pitchChange < 270 and self.pitchChange != 0:
                self.leftRightFish(1)
            else: 
                self.leftRightFish(0)
            return True

        if self.yPosition > yLimit - xymargin:
            # print("y high")
            if self.pitchChange >= 180 or self.pitchChange == 0:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
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


# like the community peaceful fish
class Fish(EverythingFish):

    def __init__(self, fishType, tankDims):
        EverythingFish.__init__(self, fishType, tankDims)

    # create a sequence, a loop of functions. call the superclasses' methods
    # to add to the sequence of these fish
    def move(self):
        if not self.isMoving:
            self.isMoving = True
            self.seq = Sequence()
            self.moveStraight()
            self.seq.append(Func(self.UDLRFish))
            self.seq.loop()




# make aggressive fish
class AggressiveFish(EverythingFish):
    def __init__(self, fishType, position, tankDims, fishList):
        EverythingFish.__init__(self, fishType, position, tankDims)
        self.fishList = fishList

    # see if any fish are minDistance away, and the closest fish at that
    def chasable(self):
        minDistance = 10
        chasedFish = None
        for fish in self.fishList:
            dist = ((fish.xPosition - self.xPosition)**2 + (fish.yPosition - 
                self.yPosition)**2 + (fish.zPosition - self.zPosition)**2)**0.5
            if dist < minDistance:
                chasedFish = fish
                minDistance = dist
        return chasedFish

    # to find pitchChange (direction fish needs to turn towards) to chase
    # another fish
    def findPitchChange(self):
        if self.xyChange == [0, -1]: self.pitchChange = 0
        elif self.xyChange == [+1, -1]: self.pitchChange = 45
        elif self.xyChange == [+1, 0]: self.pitchChange = 90
        elif self.xyChange == [+1, +1]: self.pitchChange = 135
        elif self.xyChange == [0, +1]: self.pitchChange = 180
        elif self.xyChange == [-1, +1]: self.pitchChange = 225
        elif self.xyChange == [-1, 0]: self.pitchChange = 270
        elif self.xyChange == [-1, -1]: self.pitchChange = 315

    # change the way the Fish's x, y, and z change to follow the 
    # chasableFish
    def chaseFish(self, chasableFish):
        fish = chasableFish
        self.xyChange = [self.xChange, self.yChange]
        if fish.xPosition - self.xPosition > 0: self.xyChange[0] = +1
        elif fish.xPosition - self.xPosition < 0: self.xyChange[0] = -1

        if fish.yPosition - self.yPosition > 0: self.xyChange[1] = +1
        elif fish.yPosition - self.yPosition < 0: self.xyChange[1] = -1

        if fish.zPosition - self.zPosition > 0: 
            self.zChange = +1
            self.headingChange = -30
        elif fish.zPosition - self.zPosition < 0: 
            self.zChange = -1
            self.headingChange = +30

        self.xChange, self.yChange = self.xyChange[0], self.xyChange[1]
        self.findPitchChange()

        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    def UDLRFish(self):
        chasableFish = self.chasable()
        if chasableFish != None:
            self.chaseFish(chasableFish)
        else:
            # super(AggressiveFish, self).UDLRFish(self)
            EverythingFish.UDLRFish(self)

    def move(self):
        self.seq = Sequence()
        self.moveStraight()
        self.seq.append(Func(self.UDLRFish))
        self.seq.loop()



# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
tank = fishTank()  # Create an instance of our class
tank.run()  # Run the simulation


