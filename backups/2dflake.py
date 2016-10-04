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

from pandac.PandaModules import WindowProperties
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-title YourAquarium")
loadPrcFileData("", "win-size 1280 760")
loadPrcFileData("", "win-origin 0 0")

from direct.task.Task import Task

import random
import copy

# FYI: some of the uncommented code is for my own testing purposes




class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        # Set up key input, borrowed
        self.accept('escape', sys.exit)

        self.topX = -.3
        base.setBackgroundColor(0, 0, 0) # set background black

        self.fishList = []
        self.splashScreen()

        self.mousing = False

    def splashScreen(self):
        self.title = OnscreenText(text="YourAquarium", fg=(1, 1, 1, 1),
            shadow=(0, 0, 0, .5), scale=.1, pos = (0,.1))
        self.aqSim = DirectButton(text = ("Aquarium Simulation"), scale = 0.06,
            command = self.aqSplash, pos = (0,0,-1), parent = base.a2dTopCenter)
        try:
            self.escape.setText("Press ESC to quit.")
        except:
            self.escape = OnscreenText(text="Press ESC to quit.", fg = (1,1,1,1),
            scale = 0.06, pos = (+.1,-.1), align = TextNode.ALeft, mayChange = 1,
            parent = base.a2dTopLeft)

    def createTank(self):
        # loader.loadModel borrowed from Panda3D's first program example
        # models from Blender
        self.sides = self.loader.loadModel("models/tanksides_03")
        # set texture from image
        sidesTex = loader.loadTexture("tex/blue.png")
        self.sides.setTexture(sidesTex)
        # attach the model to render so it appears in window
        self.sides.reparentTo(self.render2)

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
        self.bottom.reparentTo(self.render2)
        self.bottom.setScale(self.tankScale, self.tankScale, self.tankScale)
        self.bottom.setPos(0,0,0)

        # create wood decoration
        # borrowed wood model and texture
        # self.wood = self.loader.loadModel("models/wood_0")
        # woodTex = loader.loadTexture("tex/L1.jpg")
        # self.wood.setTexture(woodTex)
        # self.wood.reparentTo(self.render2)
        # self.wood.setScale(20,20,20)
        # self.wood.setPos(11, -3, 0)
        # self.wood.setHpr(30,0,0)

        # borrowed bush model and texture
        self.bush = self.loader.loadModel("models/bush_0")
        bushTex = loader.loadTexture("tex/forestGreen.png")
        self.bush.setTexture(bushTex)
        self.bush.reparentTo(self.render2)
        self.bush.setScale(20,20,20)
        self.bush.setPos(15,-8,0)

        # borrowed rock model and texture
        self.rock = self.loader.loadModel("models/rock_0")
        rockTex = loader.loadTexture("tex/rock.jpg")
        self.rock.setTexture(rockTex)
        self.rock.reparentTo(self.render2)
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
        self.render2.attachNewNode(self.fog)
        self.render2.setFog(self.fog)
        # ] end citation

        # get the dimensions (scale, width, height, length of present tank)
        self.tankDims = self.getTankDims()

    def getTankDims(self):
        return self.tankScale, self.tankLength, self.tankWidth, self.tankHeight

    def setUpWindow(self):
        # create a new window to display the graphics
        # wp = WindowProperties()
        # wp.setSize(800, 500)
        # wp.setOrigin(500, 0)
        self.render2 = NodePath("render2")
        self.render2.reparentTo(self.render)
        # win2 = base.openWindow(props = wp, type='onscreen', keepCamera=False, 
        #     makeCamera = True, requireWindow = True, scene = self.render2)
        # base.setupMouse(win2)
        # set initial camera position
        base.disableMouse()  # Disable mouse-based camera-control
        # x, y, z is actually i, k, j Position the camera
        base.camera.setPosHpr(0,-150,38,0,-10,0)
        # This code puts the standard title and instruction text on screen
        # format borrowed

    #clear the text; borrowed from Panda3D's DirectEntry module
    def clearText(self):
        self.b.enterText('')

    # when user is asked for a name input for their fish, it appears at the top
    # syntax from Panda3D
    def setText(self, nameEntered):
        self.topFishList += [OnscreenText(text = nameEntered, pos = (self.topX+.13, -.27),
            scale = 0.05, fg = (1,1,1,1), parent = base.a2dTopLeft, align = TextNode.ALeft)]
        self.currName = nameEntered

    # user selects a fish to put in the tank
    # depending which one is selected, an image of that fish will appear in the
    # top left corner
    def setFish(self, fishType):
        self.topX += .5
        self.currentFish = fishType

        if fishType == "blue tang":
            textt = "Blue Tang"
            # image of the fish at the top left. Syntax from Panda3D
            self.topFishList += [OnscreenImage(image = 'pics/blueTang.png', 
            pos = (self.topX, 0, -.3), scale = 0.1, parent = base.a2dTopLeft)]

        if fishType == "sailfin tang":
            textt = "Sailfin Tang"
            self.topFishList+=[OnscreenImage(image = 'pics/sailfinTang2.png', 
            pos = (self.topX, 0, -.3), scale = 0.08, parent = base.a2dTopLeft)]

        if fishType == "yellow tang":
            textt = "Yellow Tang"
            self.topFishList += [OnscreenImage(image = 'pics/yellowTang2.png',
            pos = (self.topX, 0, -.3), scale = 0.08, parent = base.a2dTopLeft)]

        if fishType == "clown fish":
            textt = "Clown Fish"
            self.topFishList += [OnscreenImage(image = 'pics/clownFish4.png', 
            pos = (self.topX, 0, -.3), scale = 0.08, parent = base.a2dTopLeft)]


        # Entry for a name. Syntax from Panda3D
        self.b = DirectEntry(text = "" ,scale=.045,command=self.setText,
        initialText="Name:", numLines = 1,focus=0, width = 6,
        focusInCommand=self.clearText, pos = (0,0,+.3), parent = base.a2dBottomCenter)

        # Menu for what type of fish
        self.menu = DirectOptionMenu(text="type", scale=0.05,items=
            ["Community","Aggressive"], highlightColor=(0.65,0.65,0.65,1), 
            pos = (0,0,+.2), command=self.selectType, parent = base.a2dBottomCenter)

    def selectType(self, typeFish):
        self.addButt = DirectButton(text = ("Add"), extraArgs = [typeFish],
            scale = 0.05, command = self.addFish, pos = (+.05, 0, +.1),
            parent = base.a2dBottomCenter)
    
    # add the fish to the list and create it in the tank
    # Put the type of fish at the top left
    def addFish(self, typeFish):
        if typeFish == "Community":
            self.fishList += [Fish(self.currentFish, self.tankDims, 
                self.currName, self.render2)]
        elif typeFish == "Aggressive": 
            prevList = self.fishList
            self.fishList += [AggressiveFish(self.currentFish, self.tankDims,
                prevList, self.currName, self.render2)]
        self.topFishList += [OnscreenText(text = typeFish, pos = (self.topX+.13, -.32),
            scale = 0.05, fg = (1,1,1,1), parent = base.a2dTopLeft, align = TextNode.ALeft)]
        self.currName = ""
        # remove the menus when done creating a fish
        self.addButt.destroy()
        self.b.destroy()
        self.menu.destroy()

    # borrowed syntax for isPlaying and pause
    # making things move and not move
    def stop(self):
        self.playButt.destroy()
        self.playButt = DirectButton(text = ("Run", "", "Run?", "disabled"), 
            scale = 0.08, command = self.moveFish, pos = (-.25, 0, +.2),
            parent = base.a2dBottomRight)
        for fish in self.fishList:
            if fish.seq.isPlaying():
                fish.seq.pause()

    def moveFish(self):
        print("moving")
        self.playButt = DirectButton(text = ("Run"), scale = 0.08, 
            pos = (-.25, 0, +.2), parent = base.a2dBottomRight, 
            command = self.stop, frameColor = (0,100,50,1))
        for fish in self.fishList:
            try: # if paused
                fish.seq.loop()
            except: # start the sequence and movement
                fish.move()

    # GUI for making an fish images
    def fishImages(self):
        # GUI things
        self.tangObject = OnscreenImage(image = 'pics/blueTang.png', 
            pos = (.2, 0, +.28), scale = 0.1, parent = base.a2dBottomLeft)
        self.sailfinObject = OnscreenImage(image = 'pics/sailfinTang2.png', 
            pos = (.55, 0, +.28), scale = 0.08, parent = base.a2dBottomLeft)
        self.yellowObject = OnscreenImage(image = 'pics/yellowTang2.png', 
            pos = (.9, 0, +.28), scale = 0.08, parent = base.a2dBottomLeft)
        self.nemoObject = OnscreenImage(image = 'pics/clownFish4.png', 
            pos = (1.25, 0, +.28), scale = 0.08, parent = base.a2dBottomLeft)

    # destroy all the GUI elements on screen
    def backspace(self):
        for fish in self.fishList:
            fish.remove()
        for obj in self.topFishList:
            obj.remove_node()
        self.tangObject.destroy()
        self.sailfinObject.destroy()
        self.yellowObject.destroy()
        self.nemoObject.destroy()
        self.bTButt.destroy()
        self.sFButt.destroy()
        self.yTButt.destroy()
        self.cFButt.destroy()
        self.playButt.destroy()
        self.feedButt.destroy()
        self.yourFish.destroy()
        self.sides.remove_node()
        self.bottom.remove_node()
        self.rock.remove_node()
        self.bush.remove_node()
        self.topX = -.3
        self.splashScreen()

    # DirectGUI interface from Panda3D. Looked at its syntax for DirectButtons
    # GUI begins by selecting a fish and then customizing that fish.
    def aqSplash(self):
        # GUI outside the classes, so can happen any time
        self.aqSim.destroy()
        self.title.destroy()
        self.escape.setText("Press backspace to return.")
        self.accept("backspace", self.backspace)
        self.setUpWindow()
        self.createTank()
        self.topFishList = []
        self.makeFishButt = DirectButton(text = ("Add Fish"), parent = base.a2dTopCenter,
            pos = (0, 0, -.2), command = self.addfishGUI, scale = 0.07)

    def addfishGUI(self):
        self.makeFishButt.destroy()
        self.fishImages()

        self.yourFish = OnscreenText(text = "Your Fish:", pos = (+.1,-.2),
            scale = 0.07, fg = (1,1,1,1), align = TextNode.ALeft, parent = base.a2dTopLeft)
        self.bTButt = DirectButton(text = ("Blue Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["blue tang"], 
            pos = (.2,0,+.15), parent = base.a2dBottomLeft)
        self.sFButt = DirectButton(text =("Sailfin Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["sailfin tang"],
             pos = (.55,0,+.15), parent = base.a2dBottomLeft)
        self.yTButt = DirectButton(text =("Yellow Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["yellow tang"],
            pos = (.9,0,+.15), parent = base.a2dBottomLeft)
        self.cFButt = DirectButton(text =("Clown Fish"),
            scale = 0.05, command = self.setFish, extraArgs = ["clown fish"], 
            pos = (1.25,0,+.15), parent = base.a2dBottomLeft)

        self.playButt = DirectButton(text = ("Run", "", "Run?", "disabled"), 
            scale = 0.08, command = self.moveFish, pos = (-.25, 0, +.2),
            parent = base.a2dBottomRight)

        self.feedButt = DirectButton(text = ("Feed fish"), scale = 0.08,
            command = self.feedFish, pos = (+.6, 0, +.25), parent = base.a2dBottomCenter)

    def feedFish(self):
        print("FEEEDDDDing")
        self.foodpic = OnscreenImage(image = "pics/fishfood.png", 
            pos = (+.6,0,+.1), scale = 0.1, parent = base.a2dBottomCenter)
        base.camera.setPosHpr(0,0,200,0,-90,0)
        self.feedTask()
        self.switchCamButt = DirectButton(text = ("View Tank"), scale = 0.08,
            command = self.switchCam, pos = (+.85, 0, +.25), parent = base.a2dBottomCenter)

    def switchCam(self):
        base.camera.setPosHpr(0,-150,38,0,-10,0)
        self.foodpic.destroy()


    def feedTask(self):
        self.flakeX, self.flakeY = 0, 0
        # self.flakeIm = OnscreenImage(image = "pics/flake.png", scale = 0.08,
        #     pos = (self.flakeX, self.flakeY, 0))



        self.mousing = True
        taskMgr.add(self.feeding, "Feeding")

    def pieceSet(self):
        self.flakeIm.setHpr(0,90,0)
        self.mousing = False

    # borrowed method and modified from Panda 3D's looking-and-gripping example
    # model program
    def feeding(self, task):
        # Check to make sure the mouse is readable
        self.accept("mouse1", self.pieceSet)
        if self.mousing == False:
            return Task.done
        if base.mouseWatcherNode.hasMouse():
            # get the mouse position as a LVector2. The values for each axis are from -1 to
            # 1. The top-left is (-1,-1), the bottom right is (1,1)
            self.flakeX=base.mouseWatcherNode.getMouseX()
            self.flakeY=base.mouseWatcherNode.getMouseY()
            self.flakeIm.setPos(self.flakeX*1.4, 30, self.flakeY*1.2)



        return Task.cont




# fish class for each instance of the fish
# need to specify what type, which position
# everythingFish contains all the methods necessary for a Fish
# contains more than 1 fish needs, so it's the superclass of Fish
class EverythingFish(fishTank):

    def __init__(self, typeFish, tankDims, name, render):
        self.tankScale, self.tankLength, self.tankWidth, self.tankHeight = tankDims
        self.name = name
        self.render2 = render
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
        self.fishR.reparentTo(self.render2)
        self.fishR.setScale(1.5,1.5,1.5)

        # create alternate fish the left tail position (from fish perspective)
        self.fishL = loader.loadModel(fishModel[1])
        self.fishL.setTexture(fishTex)
        self.fishL.reparentTo(self.render2)
        self.fishL.setScale(1.5,1.5,1.5)
        
        self.fishFront = loader.loadModel(fishModel[2])
        self.fishFront.setTexture(fishTex) # use same previous fishTex
        self.fishFront.reparentTo(self.render2)
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

    def remove(self):
        self.fishR.removeNode()
        self.fishL.removeNode()
        self.fishFront.removeNode()


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

    # keep the fish within the limits of the tank
    # up and down positions were easy because you move the fish down/up
    # repectively.
    # For avoiding the sides of the wall, you need to keep into account the 
    # present orientation of the fish to turn it the way it is already pointing.
    # Also need to avoid endless loops when turning away.
    def checkBounds(self):
        zLimit = self.tankHeight*self.tankScale
        xLimit = self.tankScale*self.tankLength
        yLimit = self.tankScale*self.tankWidth
        zmargin, xymargin = 5, 10
        if self.zPosition < zmargin - 1: # actual basically bottom is 4
            # print("z low")
            self.upDownFish(0) # make fish move up
            return True
        if self.zPosition > zLimit - zmargin: # actual basically top is 30
            # print("z high")
            self.upDownFish(1)
            return True

        # hitting right wall of the tank
        if self.xPosition > xLimit - xymargin:
            # already hitting tank at a right-based angle, so turn more right
            if self.pitchChange < 90:
                self.leftRightFish(1)
            # hitting tank headon or at left-based angle, turn more left
            else: self.leftRightFish(0)
            return True

        # hitting left wall
        if self.xPosition < -xLimit + xymargin:
            # print("x low")
            if self.pitchChange < 270 and self.pitchChange != 0:
                self.leftRightFish(1)
            else: 
                self.leftRightFish(0)
            return True

        # hitting front wall
        if self.yPosition > yLimit - xymargin:
            # print("y high")
            if self.pitchChange >= 180 or self.pitchChange == 0:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
            return True

        # hitting back wall
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

    def __init__(self, fishType, tankDims, name, render):
        EverythingFish.__init__(self, fishType, tankDims, name, render)

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
    def __init__(self, fishType, tankDims, fishList, name, render):
        EverythingFish.__init__(self, fishType, tankDims, name, render)
        self.chaseList = fishList
        self.chasableFish = None
        print(self.name)

    # make sure not chasing themselves
    def __eq__(self, other):
        return (isinstance(other, EverythingFish) and (self.xPosition == 
            other.xPosition) and (self.yPosition == other.yPosition) and
            (self.zPosition == other.zPosition) and (self.name == other.name))

    # see if any fish are minDistance away, and the closest fish at that
    def chasable(self):
        minDistance = 30
        tinyDist = 6
        chasedFish = None
        for fish in self.chaseList:
            if fish != self:
                dist = ((fish.xPosition - self.xPosition)**2 + (fish.yPosition - 
                    self.yPosition)**2 + (fish.zPosition - self.zPosition)**2)**0.5
                # closest fish that is within the minDistance required to chase
                if dist < minDistance:
                    chasedFish = fish
                    minDistance = dist
                # try to make the other fish go faster
                if dist < tinyDist:
                    fish.xChange *= 1.5
                    fish.yChange *= 1.5
                    fish.zChange *= 1.5
        return chasedFish

    # to find pitchChange (direction fish needs to turn towards) to chase
    # another fish given a xyChange
    def findPitchChange(self):
        if self.tempxyChange == [0, -1]: return 0
        elif self.tempxyChange == [+1, -1]: return 45
        elif self.tempxyChange == [+1, 0]: return 90
        elif self.tempxyChange == [+1, +1]: return 135
        elif self.tempxyChange == [0, +1]: return 180
        elif self.tempxyChange == [-1, +1]: return 225
        elif self.tempxyChange == [-1, 0]: return 270
        elif self.tempxyChange == [-1, -1]: return 315
        return self.pitchChange

    # change the way the Fish's x, y, and z change to follow the 
    # chasableFish
    def chaseFish(self):
        fish = self.chasableFish
        self.xyChange = [0,0]
        # depending where the other fish, can only change one xy by one
        if fish.xPosition - self.xPosition > 0: self.xyChange[0] = +1
        elif fish.xPosition - self.xPosition < 0: self.xyChange[0] = -1
        else: self.xyChange[0] = 0

        if fish.yPosition - self.yPosition > 0: self.xyChange[1] = +1
        elif fish.yPosition - self.yPosition < 0: self.xyChange[1] = -1
        else: self.xyChange[1] = 0


        # can change both zChange and Position (up/down less complicated)
        if fish.zPosition - self.zPosition > 3: 
            if self.headingChange > -30:
                self.headingChange -= 30
            if self.headingChange == -30:
                self.zChange = +1
        elif fish.zPosition - self.zPosition < -3: 
            if self.headingChange < 30:
                self.headingChange += 30
            if self.headingChange == 30:
                self.zChange = -1
        else: 
            self.headingChange = 0
            self.zChange = 0

        self.tempxyChange = [self.xyChange[0], self.xyChange[1]]
        # find the needed rotation for this xyChange to look realistic
        neededPitch = self.findPitchChange()

        if (neededPitch - self.pitchChange > 0 or 
            (neededPitch-self.pitchChange < 0 and neededPitch-self.pitchChange >= -180)):
            self.pitchChange = (self.pitchChange + 45) % 360
        if ((neededPitch - self.pitchChange < 0 and neededPitch - self.pitchChange > -180)
         or neededPitch - self.pitchChange > 180):
            self.pitchChange = (360 + self.pitchChange - 45)%360

        self.findXYChange()

        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))

    def possChase(self):
        self.chasableFish = self.chasable()
        if self.chasableFish != None:
            print("chasing")
            self.chaseFish()

    def UDLRFishNew(self):
        if self.chasableFish == None:
            self.UDLRFish()
        else: self.possChase()

    def move(self):
        self.seq = Sequence()
        self.seq.append(Func(self.UDLRFishNew))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailCenter))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailLeft))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.possChase))
        self.seq.append(Func(self.moveTailCenter))
        self.seq.append(Wait(.15))
        self.seq.append(Func(self.moveTailRight))
        self.seq.loop()

    # def move(self):
    #     self.seq = Sequence()
    #     self.moveStraight()
    #     self.seq.append(Func(self.UDLRFish))
    #     self.seq.loop()



# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
tank = fishTank()  # Create an instance of our class
tank.run()  # Run the simulation


