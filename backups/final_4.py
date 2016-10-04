# Christina Ou
# AndrewID: cou
# TERM PROJECT
# previous files and versions are in backups folder
# Used Panda3D and Blender
# Blender to create the models which are borrowed from Turbosquid's users
#   and to position the models to simulate moving

# Using Panda3D's libraries to enact the 3D model of my aquarium

# Aquarium

# Panda imports to enable what I'm doing
# Following import ideas are borrowed from user forums or Panda3D manual
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, NodePath
from direct.showbase.DirectObject import DirectObject

# for Panda3D's DirectGUI
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *

import sys # not super sure.. probably for showbase.__init__
# for the sequencing
from direct.interval.IntervalGlobal import *
# fog for depth perception
from panda3d.core import Fog

# for creating a basically full-size window screen
from pandac.PandaModules import *
loadPrcFileData("", "window-title YourAquarium")
loadPrcFileData("", "win-size 1280 760")
loadPrcFileData("", "win-origin 0 0")

from panda3d.core import TransparencyAttrib # for picture transparency
# task for the mouse
from direct.task.Task import Task

import random





# DirectGUI Objects class holds almost all of my GUI items: text and images.
# I start off creating all of them and then hiding all of them.
# As the program runs, different DirectGUI objects will be shown and hidden
# I initialized all the DirectGUI Objects first so that the user can 
# exit the program at any random time and not have the program crash becauuse
# certain elements hadn't been created yet

# I have 49 DirectGUI Objects, so the user interface was actually pretty
# complicated and I spent a long time perfecting it so that only the buttons
# the user could use at the time would show up, and also that the user could
# quit at any time with any combination of buttons on the screen and not crash
class DirectGUIObjects(object):
    def __init__(self):
        self.GUIObjs = []
        self.DirectGUIImages() # make the DirectGUI images
        self.DirectGUIText() # make the DirectGUI onscreenTexts
        self.hideAll()

    def hideAll(self):
        for element in self.GUIObjs:
            element.hide()

    def destroyAll(self):
        for element in self.GUIObjs:
            element.destroy()

    def retrieveDirectGUI(self):
        return self.GUIObjs

###
### DirectGUI Images
    def colorImages(self):
        self.viewBack = OnscreenImage(image = 'pics/grayBlue.png',
            pos = (-.2,0,.15), parent = base.a2dBottomCenter, 
            scale=(.3,0,.15))
        self.runBack = OnscreenImage(image = 'pics/lightBlue.png', 
            pos = (-.23, 0, +.15), scale = (0.22,0,0.15), 
            parent = base.a2dBottomRight)
        self.firstAddBack = OnscreenImage(image = 'pics/grayBlue.png',
            pos = (.8, 0, +.15), scale = (0.45,0,0.15), 
            parent = base.a2dBottomCenter)
        self.chooseBack = OnscreenImage(image = 'pics/medPurp.png', 
            pos = (.5, 0, .15), scale = (0.93,0,0.15), 
            parent = base.a2dBottomLeft)
        self.menuBack = OnscreenImage(image = 'pics/grayBlue.png',
            pos = (.5,0,+.15), parent = base.a2dBottomCenter, scale=(.6,0,.15))
        self.foodBack = OnscreenImage(image = 'pics/medPurp.png',
            pos=(+.35,0,+.15), parent=base.a2dBottomCenter, scale=(.17,0,.15))
        self.GUIObjs += ([self.viewBack] + [self.runBack] + [self.firstAddBack]
            + [self.chooseBack] + [self.menuBack] + [self.foodBack])
        self.moreImages()

    def moreImages(self):
        self.camBack = OnscreenImage(image = 'pics/medPurp.png', 
            pos = (-.08, 0, +1.05), scale = (0.25,0, .32), 
            parent = base.a2dBottomRight)
        self.topBack = OnscreenImage(image = 'pics/medPurp.png',
            pos = (-.5,0,-.1), parent = base.a2dTopCenter, scale=(.4,0,.1))
        self.addBack = OnscreenImage(image = 'pics/grayBlue.png',
            pos = (.9, 0, +.15), scale = (0.26,0,0.15),
            parent = base.a2dBottomCenter)
        self.splashBack = OnscreenImage(image = 'pics/medPurp.png', 
            pos = (0,0,+.3), scale = (0.925,0,.4), 
            parent = base.a2dBottomCenter)
        self.GUIObjs += ([self.topBack] + [self.camBack] + [self.addBack] +
            [self.splashBack])

    # syntax for DirectGUIImages from Panda3D's manual
    def DirectGUIImages(self):
        self.colorImages()
        self.tangObject = OnscreenImage(image = 'pics/blueTang.png', 
            pos = (.2, 0, +.17), scale = 0.1, parent = base.a2dBottomLeft)
        self.tangObject.setTransparency(TransparencyAttrib.MAlpha)
        self.sailfinObject = OnscreenImage(image = 'pics/sailfinTang2.png', 
            pos = (.55, 0, +.17), scale = 0.075, parent = base.a2dBottomLeft)
        self.sailfinObject.setTransparency(TransparencyAttrib.MAlpha)
        self.yellowObject = OnscreenImage(image = 'pics/yellowTang2.png', 
            pos = (.9, 0, +.17), scale = 0.08, parent = base.a2dBottomLeft)
        self.yellowObject.setTransparency(TransparencyAttrib.MAlpha)
        self.nemoObject = OnscreenImage(image = 'pics/clownFish4.png', 
            pos = (1.25, 0, +.17), scale = 0.08, parent = base.a2dBottomLeft)
        self.nemoObject.setTransparency(TransparencyAttrib.MAlpha)
        self.foodpic = OnscreenImage(image = "pics/fishfood.png", 
            pos = (+.35,0,+.18), scale = 0.08, parent = base.a2dBottomCenter)
        self.foodpic.setTransparency(TransparencyAttrib.MAlpha)
        self.backpic = OnscreenImage(image = "pics/background.jpg",
            pos = (0,0,+.4), scale = (.8,0,.4))
        self.GUIObjs += ([self.tangObject] + [self.sailfinObject] + 
            [self.yellowObject] + [self.nemoObject] + [self.foodpic] + 
            [self.backpic])



###
### DirectGUI Text
    # syntax for DirectGUIText from Panda3D's manual
    def DirectGUIText(self):
        self.title = OnscreenText(text="YourAquarium", fg=(1, 1, 1, 1),
            shadow=(0, 0, 0, .5), scale=.1, pos = (0,-.2))
        self.start = OnscreenText(text = 
            """Welcome to the 3-D Aquarium Simulator!\n
Press Aquarium Simulation to begin creating your own aquarium.""",
            fg = (1,1,1,1), scale = 0.06, pos = (0,+.4), 
            parent = base.a2dBottomCenter)
        self.yourFish = OnscreenText(text = "Your Fish:", pos = (+.1,-.19),
            scale = 0.07, fg = (1,1,1,1), align = TextNode.ALeft, 
            parent = base.a2dTopLeft)
        self.pickFish = OnscreenText(text = 
            "Add your first Fish!\nClick add fish to get started.",
            scale = 0.05, pos = (+.45,+.13), fg = (1,1,1,1),
            parent = base.a2dBottomCenter, align = TextNode.ALeft)
        self.addFishText = OnscreenText(text = "Choose a fish to add:", 
            pos = (.1,+.25), align = TextNode.ALeft, 
            parent = base.a2dBottomLeft, scale = 0.05, fg = (1,1,1,1))
        self.GUIObjs += ([self.title] + [self.start] + [self.yourFish] + 
            [self.pickFish] + [self.addFishText])
        self.moreText()

    def moreText(self):
        self.nameFish = OnscreenText(text = """Type in a name for your fish""",
            fg = (1,1,1,1), scale = 0.04, pos = (+.35,+.24), 
            parent = base.a2dBottomCenter, align = TextNode.ALeft)
        self.pickType = OnscreenText(text = 
            """Use the menu to select the fish's type""",
            fg = (1,1,1,1), scale = 0.04, pos = (+.35,+.135), 
            parent = base.a2dBottomCenter, align = TextNode.ALeft)
        self.addingFish = OnscreenText(text="""Add your new fish!""",
            fg = (1,1,1,1),scale = 0.04, pos = (+.35,+.05), 
            parent = base.a2dBottomCenter,align = TextNode.ALeft)
        self.runText = OnscreenText(text = "Hit run to start\nthe simulation!",
            fg = (0,0,0,1),scale = 0.04, pos = (-.25, +.225), 
            parent = base.a2dBottomRight)
        self.pauseText = OnscreenText(text = "Press to pause", 
            fg = (0,0,0,1), scale = 0.04, pos = (-.25, +.225),
            parent = base.a2dBottomRight)
        self.GUIObjs += ([self.nameFish] + [self.pickType] + [self.addingFish] 
            + [self.runText] + [self.pauseText])
        self.evenMoreText()

    def evenMoreText(self):
        self.camText = OnscreenText(text = "Toggle Camera\nScreen View", 
            fg = (1,1,1,1), scale = 0.04, pos = (-.17, +1.25), 
            parent = base.a2dBottomRight)
        self.topText = OnscreenText(text = 
            "Select fish from\nYour Fish to view from", 
            fg = (1,1,1,1), scale = 0.05, pos = (-.5, -.1), 
            parent = base.a2dTopCenter)
        self.escape=OnscreenText(text="Press ESC to quit.", fg = (1,1,1,1),
            scale = 0.06, pos = (+.1,-.1), align=TextNode.ALeft,
            parent = base.a2dTopLeft)
        self.fishViewText = OnscreenText(text = 
            """Try selecting different fish\nfrom above or try feeding""",
            fg = (1,1,1,1), scale = 0.04, pos = (-.2,+.1),
            parent = base.a2dBottomCenter)
        self.GUIObjs += ([self.camText] + [self.topText] + [self.escape] +
            [self.fishViewText])
        self.extraEvenMoreText()

    def extraEvenMoreText(self):
        self.userViewText = OnscreenText(text = 
            """Use up, down, left, and right\narrows to move fish""",
            fg = (1,1,1,1), scale = 0.04, pos = (-.2,+.1),
            parent = base.a2dBottomCenter)
        self.commAggText = OnscreenText(text = """Community fish are peaceful
and have randomized movements.\n\nAggressive fish chase other fish
when they get close enough.""", fg =(1,1,1,1), scale = 0.035, pos = (-.55,+.2),
            parent = base.a2dBottomRight, align = TextNode.ALeft)
        self.GUIObjs += [self.userViewText] + [self.commAggText]






class fishTank(ShowBase):
### 
### INITIAL
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class
        self.splashScreen()

    # like init function to return to splashScreen
    def splashScreen(self):
        # make all of the DirectGUI Objects
        self.dirGUI = DirectGUIObjects()
        self.moreDirGUI = [] # directGUI objects from THIS class
        self.setUpButtons() # set up all the DirectGUI buttons needed later
        self.setUpEntries() # set up all the DirectGUI entry items
        for obj in self.moreDirGUI:
            obj.hide() # start with no DirectGUI items
        # for spacing
        self.topX,self.userFishIndex = -.3, None
        base.setBackgroundColor(0, 0, 0) # set background black

        self.displayRegion = None
        self.makingUserFish = False
        self.haveUserFish, self.fishViewing = False, False
        self.mousing = False
        # set the list of fishes and flakes in the tank
        self.fishList = []
        self.flakeList = []
        self.viewButtList = []

        self.dirGUI.splashBack.show() # background
        self.dirGUI.backpic.show() #background
        self.aqSim.show() # button to start simulation
        # ESC quits everything
        self.dirGUI.title.show() # text of title of project
        self.dirGUI.start.show() # text with start description



###
### BUTTONS
    # collection for all of my buttons
    # most if not all of the buttons perform an action
    # I commented what action button has further down in the code when the
    # button is activated
    # syntax for DirectGUI buttons from Panda3D manual
    def setUpButtons(self):
        self.aqSim = DirectButton(text = ("Aquarium Simulation"), scale = 0.06,
            command = self.aqSplash,pos=(0,0,.55),parent=base.a2dBottomCenter)
        self.makeFishButt = DirectButton(text = ("Add Fish"), 
            parent = base.a2dBottomCenter, pos = (.6, 0,+.2), 
            command = self.addfishGUI, scale = 0.07)
        self.switchCamAer = DirectButton(text = ("Aerial View"), scale = 0.05,
            command = self.switchAer, pos = (-.17, 0, +1), 
            parent = base.a2dBottomRight)
        self.switchCamFront = DirectButton(text = ("Front View"), scale=0.05,
            command = self.switchFront, pos = (-.17, 0, +1), 
            parent = base.a2dBottomRight)
        self.camUpButt = DirectButton(text = ("Up"), scale = 0.04,
            command = self.upCam, pos = (-.17, 0, +1.1), 
            parent = base.a2dBottomRight)
        self.camDownButt = DirectButton(text = ("Down"), scale = 0.04,
            command = self.downCam, pos = (-.17, 0, +.9), 
            parent = base.a2dBottomRight)  

        self.moreDirGUI+=([self.aqSim]+[self.makeFishButt]+[self.switchCamAer]+
        [self.switchCamFront] + [self.camUpButt] + [self.camDownButt])

        self.moreButtons()

    # more buttons!
    # all of the buttons are chronological
    # RIP top-down design sorry but many things are sequential and it was
    # easier for me to see things that way
    def moreButtons(self):
        self.bTButt = DirectButton(text = ("Blue Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["blue tang"], 
            pos = (.2,0,+.04), parent = base.a2dBottomLeft)
        self.sFButt = DirectButton(text =("Sailfin Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["sailfin tang"],
             pos = (.55,0,+.04), parent = base.a2dBottomLeft)
        self.yTButt = DirectButton(text =("Yellow Tang"),
            scale = 0.05, command = self.setFish, extraArgs = ["yellow tang"],
            pos = (.9,0,+.04), parent = base.a2dBottomLeft)
        self.cFButt = DirectButton(text =("Clown Fish"),
            scale = 0.05, command = self.setFish, extraArgs = ["clown fish"], 
            pos = (1.25,0,+.04), parent = base.a2dBottomLeft)

        self.playButt = DirectButton(text = ("Run", "", "Run?", "disabled"), 
            scale = 0.07, command = self.moveFish, pos = (-.25, 0, +.1),
            parent = base.a2dBottomRight)

        self.moreDirGUI += ([self.bTButt] + [self.sFButt] + [self.yTButt] + 
            [self.cFButt] + [self.playButt])
        self.evenMoreButtons()

    def evenMoreButtons(self):
        self.userFishButt = DirectButton(text = ("Add user fish"), scale=0.055,
            command = self.swimAsFish, pos = (.9, 0,+.04), 
            parent = base.a2dBottomCenter)
        self.fishViewButt = DirectButton(text = ("Fish View"), scale = 0.05,
            command = self.fishView, pos = (+.9,0,+.115), 
            parent = base.a2dBottomCenter)
        self.feedButt = DirectButton(text = ("Feed fish"), scale = 0.05,
            command = self.feedFish, pos = (+.9, 0, +.175), 
            parent = base.a2dBottomCenter)
        self.addButt2 = DirectButton(text = ("Add more fish"), scale = 0.055,
            command = self.addFish2, pos = (.9, 0,+.24), 
            parent = base.a2dBottomCenter)
        self.playButt2 = DirectButton(text = ("Run"), scale = 0.07, 
            pos = (-.25, 0, +.1), parent = base.a2dBottomRight, 
            command = self.stop, frameColor = (100,113,154,1))
        self.moreDirGUI += ([self.fishViewButt] + [self.feedButt] + 
            [self.addButt2] + [self.playButt2] + [self.userFishButt])
        self.extraEvenMoreButtons()

    def extraEvenMoreButtons(self):
        self.grabFoodButt = DirectButton(text = ("Grab Food"), scale = 0.05,
            command = self.grabFood, pos = (.35, 0,+.025), 
            parent = base.a2dBottomCenter)
        self.exitViewButt = DirectButton(text = ("Exit fish view"), 
            scale = 0.05, command = self.clearFishView, pos = (-.2, 0,+.24), 
            parent = base.a2dBottomCenter)
        self.viewFoodButt = DirectButton(text = ("Feed fish"), scale = 0.05,
            command = self.feedFish, pos = (-.2, 0, +.175), 
            parent = base.a2dBottomCenter)
        self.moreDirGUI += ([self.grabFoodButt] + [self.exitViewButt] + 
            [self.viewFoodButt])

    # syntax for DirectGUI entries and menus from Panda3D manual
    def setUpEntries(self):
        self.entry = DirectEntry(text = "" ,scale=.045,command=self.setText,
        initialText="Name:", numLines = 1,focus=0, width = 6, pos = (0,0,+.24),
        focusInCommand=self.clearText, parent = base.a2dBottomCenter)
        self.menu = DirectOptionMenu(text="type", scale=0.05,items=
            ["Community","Aggressive"], highlightColor=(0.65,0.65,0.65,1), 
            pos = (0,0,+.135), command=self.selectType, 
            parent = base.a2dBottomCenter)
        self.moreDirGUI += [self.entry] + [self.menu]



###
### WINDOW SHENANIGANS
    # DirectGUI interface from Panda3D. Looked at its syntax for DirectButtons
    # GUI begins by selecting a fish and then customizing that fish.
    def aqSplash(self):
        # hide title screen gui text objects
        self.aqSim.hide()
        self.dirGUI.title.hide()
        self.dirGUI.start.hide()
        self.dirGUI.backpic.hide()
        self.dirGUI.splashBack.hide()
        self.dirGUI.escape.show() # text saying press escape to reset
        # show first step text: picking fish, also "Your Fish: " at the top
        self.dirGUI.pickFish.show()
        self.dirGUI.camText.show()
        self.accept("escape", self.reset)
        self.setUpWindow() # set up window and camera
        self.createTank() # create tank model and its objects and fog
        self.topFishList = []
        
        self.dirGUI.firstAddBack.show() # background for first addButt
        self.dirGUI.camBack.show() # background darkPurp for camera
        self.makeFishButt.show() # button for making fish
        self.switchCamAer.show() # button for switching cam to aerial view
        self.camUpButt.show() # button for moving camera up

    def setUpWindow(self):
        self.render2 = NodePath("render2")
        self.render2.reparentTo(self.render)
        # set initial camera position
        base.disableMouse()  # Disable mouse-based camera-control
        # x, y, z is actually i, k, j Position the camera
        self.switchFront()

    # hide all the GUI elements on screen and return to splash screen
    # can't call "init" again so hardcoding init right here
    def reset(self):
        self.clearFishView()
        for fish in self.fishList:
            try: fish.seq.pause()
            except: pass
            fish.remove()
        for obj in self.topFishList:
            obj.destroy() # destroy or remove_node??
        for butt in self.viewButtList:
            butt.destroy()
        for element in self.moreDirGUI:
            element.destroy()
        self.dirGUI.destroyAll()
        # remove tank objects
        self.sides.remove_node()
        self.bottom.remove_node()
        self.rock.remove_node()
        self.bush.remove_node()
        self.splashScreen()



###
### CREATING TANK AND SETTING UP
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

        self.createDecor()

    def createDecor(self):
        # create wood decoration
        # borrowed wood model and texture
        self.wood = self.loader.loadModel("models/wood_0")
        woodTex = loader.loadTexture("tex/L1.jpg")
        self.wood.setTexture(woodTex)
        self.wood.reparentTo(self.render2)
        self.wood.setScale(20,20,20)
        self.wood.setPosHpr(11, -3, 0, 30,0,0)

        # borrowed bush model and texture
        self.bush = self.loader.loadModel("models/bush_0")
        bushTex = loader.loadTexture("tex/bush.png")
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
        self.rock.setPosHpr(-20,5,0,50,0,0)       
        self.tankDims = self.getTankDims()
        self.createFog()

    def createFog(self):
        # creating fog. borrowed from Panda3D's infinite-tunnel demo/tutorial
        # beg citation [
        # Create an instance of fog called 'distanceFog'.
        # 'distanceFog' is just a name for our fog, not a specific type of fog.
        self.fog = Fog('distanceFog')
        color = (.13, .204, .565)
        # # Me choosing fog color to be a sort of blue
        self.fog.setColor(*color)
        # Set the density/falloff of the fog.  The range is 0-1.
        # The higher the numer, the "bigger" the fog effect.
        # making fog go along y axis
        self.fog.setLinearRange(-40,40)
        self.render2.attachNewNode(self.fog)
        self.render2.setFog(self.fog)
        # ] end citation


        # get the dimensions (scale, width, height, length of present tank)

    def getTankDims(self):
        return self.tankScale, self.tankLength, self.tankWidth, self.tankHeight



###
### ADDING FISH

    def addfishGUI(self):
        self.dirGUI.runBack.hide() # background color
        self.dirGUI.firstAddBack.hide() # background color
        self.dirGUI.addBack.hide() # background color
        self.dirGUI.chooseBack.show() # background color
        self.dirGUI.pickFish.hide() # text for adding first fish
        self.makeFishButt.hide() # button to start adding a fish
        self.playButt.hide() # run buttons
        self.playButt2.hide() # can't run til finish making fish
        self.userFishButt.hide() # button to make user fish
        self.grabFoodButt.hide() # button for feeding fish

        self.fishImages() # make all the images for fish to choose to add
        self.dirGUI.addFishText.show() # "Choose a fish"

        # following buttons are to select which species of fish to add
        #### CALLS function "setFish" ####
        self.bTButt.show()
        self.sFButt.show()
        self.yTButt.show()
        self.cFButt.show()

    # GUI for making an fish images
    def fishImages(self):
        # GUI things
        self.dirGUI.tangObject.show()
        self.dirGUI.sailfinObject.show()
        self.dirGUI.yellowObject.show()
        self.dirGUI.nemoObject.show()

    # opposite of above. helpful for the different modes
    def hideFishImages(self):
        self.dirGUI.tangObject.hide()
        self.dirGUI.sailfinObject.hide()
        self.dirGUI.yellowObject.hide()
        self.dirGUI.nemoObject.hide()

    # "setFish" below's helper function
    # clearing parts of the screen and buttons to add the fish
    def prepForSetFish(self, fishType):
        self.dirGUI.chooseBack.hide() # background
        self.dirGUI.nameFish.show()
        self.bTButt.hide() # hide the species fish buttons
        self.sFButt.hide() # so user can't add more fish until 
        self.yTButt.hide() # they finish creating one fish
        self.cFButt.hide()
        self.hideFishImages()
        self.dirGUI.addFishText.hide() # hide text for adding fish
        self.currentFish = fishType
        self.topX += .5
        self.dirGUI.yourFish.show() # text listing our fish at the top
        self.dirGUI.menuBack.show()
        if fishType == "blue tang":
            textt = "Blue Tang"
            # self.topFishList collects all the top inputs. 
            # separate from our previous DirectGUI collections because
            # these inputs rely on user input and are not constant            
            pic = OnscreenImage(image = 'pics/blueTang.png', 
            pos = (self.topX, 0, -.3), scale = 0.1, parent = base.a2dTopLeft)
            pic.setTransparency(TransparencyAttrib.MAlpha)
            self.topFishList += [pic]
            self.dirGUI.tangObject.show()

    # user selects a fish to put in the tank
    # depending which one is selected, an image of that fish will appear in the
    # top left corner
    def setFish(self, fishType):
        self.prepForSetFish(fishType)
        if fishType == "sailfin tang":
            textt, img = "Sailfin Tang", 'pics/sailfinTang2.png'
            self.dirGUI.sailfinObject.show()
        if fishType == "yellow tang":
            textt = "Yellow Tang"
            img = 'pics/yellowTang2.png'
            self.dirGUI.yellowObject.show()
        if fishType == "clown fish":
            textt = "Clown Fish"
            img = 'pics/clownFish4.png'
            self.dirGUI.nemoObject.show()
        try: # in case in above helper function
            pic = OnscreenImage(image = img, pos = (self.topX, 0, -.3), 
                scale = 0.08, parent = base.a2dTopLeft)
            pic.setTransparency(TransparencyAttrib.MAlpha)
            self.topFishList+=[pic]
        except: pass
        # Entry DirectGUI element to set a name for the fish
        #### CALLS function "setText" ####
        self.entry.show()

    # when user is asked for a name input for their fish, it appears at the top
    # syntax from Panda3D
    def setText(self, nameEntered):
        self.topFishList += [OnscreenText(text = nameEntered, 
            pos = (self.topX+.13, -.27), scale = 0.05, fg = (1,1,1,1),
            parent = base.a2dTopLeft, align = TextNode.ALeft)]
        self.currName = nameEntered

        # Menu for what type of fish. select "community" or "aggressive"
        #### CALLS "selectType" ####
        if not self.makingUserFish:
            # description of community and aggressive fish
            self.dirGUI.commAggText.show()
            self.menu.show()
            # text instructions for picking the type
            self.dirGUI.pickType.show() 
        else: self.selectType("User Fish")

    #clear the text; borrowed from Panda3D's DirectEntry module
    def clearText(self):
        self.entry.enterText('')    

    def selectType(self, typeFish):
        self.dirGUI.addingFish.show() # text to say "Add this fish!"
        # button to add the fish
        # takes in the type of fish to call #### "addFish" function ####
        try: self.addButt.destroy()
        except: pass
        self.addButt = DirectButton(text = ("Add"), extraArgs = [typeFish],
            scale = 0.05, command = self.addFish, pos = (+.05, 0, +.05),
            parent = base.a2dBottomCenter)
        self.moreDirGUI += [self.addButt]
        
    # helper function to prep for "addFish" below
    # mostly clearing screen because everything to add the fish is done
    def addFishPrep(self, typeFish):
        self.dirGUI.menuBack.hide() # background color
        self.dirGUI.runBack.show() # blue backgroun for run text
        self.dirGUI.addingFish.hide() # text for adding fish
        self.dirGUI.nameFish.hide() # text for naming fish
        self.dirGUI.pickType.hide() # text for picking type of fish
        # remove the menus when done creating a fish
        self.addButt.hide() # hide add button
        self.entry.hide() # hide entry object
        self.dirGUI.commAggText.hide() # hide comm/agg descrip text
        self.menu.hide() # hide menu
        self.dirGUI.runText.show() # show text saying to run!
        self.addButt.destroy()
        self.moreDirGUI = self.moreDirGUI[:-1]
        self.hideFishImages()
        if not self.makingUserFish:
            self.dirGUI.addBack.show() # background
            self.addButt2.show() # button to add another fish if wanted
        self.playButt.show() # button to "run" the simulation
        if typeFish == "Community":
            self.fishList += [Fish(self.currentFish, self.tankDims, 
                self.currName, self.render2)]

    # add the fish to the list and create it in the tank
    # Put the type of fish at the top left
    def addFish(self, typeFish):
        self.addFishPrep(typeFish)
        if typeFish == "Aggressive": 
            prevList = self.fishList
            self.fishList += [AggressiveFish(self.currentFish, self.tankDims,
                prevList, self.currName, self.render2)]
        elif typeFish == "User Fish":
            self.fishList += [UserFish(self.currentFish, self.tankDims,
                self.currName, self.render2)]
            self.userFishIndex = len(self.fishList)-1
            self.fishView() # open up the fish view window
            self.parentCam(self.userFishIndex) # parent camera to this fish
        self.topFishList += [OnscreenText(text = typeFish, pos = 
            (self.topX+.13, -.32), scale = 0.05, fg = (1,1,1,1),
            parent = base.a2dTopLeft, align = TextNode.ALeft)]
        # viewButt comes in handy later when selecting a fish to view
        # takes in what index it's at aka which fish it's referencing
        viewButt = DirectButton(text = (self.currName), scale = 0.05, command =
            self.parentCam, extraArgs = [len(self.fishList)-1], 
            pos = (self.topX+.15, 0, -.4), parent = base.a2dTopLeft)
        viewButt.hide()
        self.currName = "" # reset what the currName is
        self.viewButtList += [viewButt] # same index as the fish

### 
### MOVE FISH WITH BUTTON
    def prepMoveFish(self):
        # hides all the bottom left images
        # not in "adding fish" mode anymore
        self.dirGUI.tangObject.hide()
        self.dirGUI.sailfinObject.hide()
        self.dirGUI.yellowObject.hide()
        self.dirGUI.nemoObject.hide()
        self.dirGUI.addFishText.hide()
        self.dirGUI.runText.hide()
        self.dirGUI.pauseText.show()
        self.dirGUI.addBack.show()

        self.bTButt.hide()
        self.sFButt.hide()
        self.yTButt.hide()
        self.cFButt.hide()

    def moveFish(self):
        self.prepMoveFish()
        if not self.haveUserFish: # make sure don't already have a user fish
            self.userFishButt.show() # mode for creating own fish to move
        self.fishViewButt.show() # mode for seeing in fish-eye view
        self.feedButt.show() # mode for feeding
        self.addButt2.show() # mode for adding more fish!
        self.playButt.hide() # hide gray run button
        # show cyan run button because simulation is running!
        self.playButt2.show() 

        # start making things move!
        for fish in self.fishList:
            # used a try in case the fish hasn't even made a sequence yet
            # try is if a fish is paused
            try: fish.seq.loop()
            # otherwise start the sequence and movement
            except: fish.move()
        for flake in self.flakeList:
            if flake != None:
                # same reason for try as above instead with the food flakes
                try: flake.seq.loop()
                except: flake.move()

    # borrowed syntax for isPlaying and pause
    # making things move and not move
    def stop(self):
        self.dirGUI.pauseText.hide()
        self.dirGUI.runText.show()
        self.playButt2.hide() # not cyan anymore because not running
        self.playButt.show() # original run button!
        for fish in self.fishList:
            try: 
                if fish.seq.isPlaying(): fish.seq.pause()
            except: pass

    # when you add more fish, hide the food pic if it is present
    # stop the simulation to add more fish
    def addFish2(self):
        if self.fishViewing:
            self.clearFishView()
        self.dirGUI.foodBack.hide() # background
        self.dirGUI.foodpic.hide() # if food pic is there from feeding remove
        self.fishViewButt.hide() # hide fish view mode button
        self.feedButt.hide() # hide feed fish mode button
        self.addButt2.hide() # hide adding another fish mode button
        self.userFishButt.hide() # hide button for user fish mode
        self.stop()
        self.dirGUI.runText.hide()
        self.addfishGUI()



###
### FISH VIEW MODE
    def hideAddMenu(self):
        self.dirGUI.addBack.hide()
        self.addButt2.hide()
        self.feedButt.hide()
        self.fishViewButt.hide()
        self.userFishButt.hide()

    def showAddMenu(self):
        self.dirGUI.addBack.show()
        self.addButt2.show()
        self.feedButt.show()
        self.fishViewButt.show()
        self.userFishButt.show()

    def prepFishView(self):
        self.hideAddMenu()
        self.grabFoodButt.hide() # hide button for grabbing food
        self.dirGUI.foodBack.hide() # backgroud
        self.dirGUI.foodpic.hide() # hide food picture
        self.dirGUI.viewBack.show()
        self.exitViewButt.show()
        self.dirGUI.fishViewText.show()
        self.fishViewing = True
        self.render2.clearFog()
        sidesTex = loader.loadTexture("tex/blue4.png")
        self.sides.setTexture(sidesTex)

    # code for making separate display region from Panda3D manual
    def makeSplitScreen(self):
        left,right,bottom,top = 0, .35, 0, .3
        self.displayRegion = base.win.makeDisplayRegion(left, right,bottom,top)
        # make a new camera for this region
        camNode = Camera('cam')
        self.camNP = NodePath(camNode)
        self.displayRegion.setCamera(self.camNP)
        # clear background to black so it doesn't overlap with normal
        # window
        self.displayRegion.setClearColor(VBase4(0, 0, 0, 1))
        self.displayRegion.setClearColorActive(True)
        self.displayRegion.setClearDepthActive(True)
        self.displayRegion.setClearDepth(1)

    # start fish view mode
    def fishView(self):
        self.prepFishView()
        # separate the region from the rest of the window
        if self.displayRegion == None:
            self.makeSplitScreen()
        # activate earlier buttons to select from which viewpoint to look
        # from
        if not self.makingUserFish:
            self.dirGUI.topBack.show()
            self.dirGUI.topText.show()
            for butt in self.viewButtList:
                butt.show()
        self.makingUserFish = False # not making anymore

    def parentCam(self, index):
        self.dirGUI.viewBack.show()
        self.exitViewButt.show()
        # get the index from the viewButton's from the top
        # index will be which fish we're looking at
        fishForCam = self.fishList[index]
        # parent of the camera will be this fishForCam
        self.camNP.reparentTo(fishForCam.fishFront) 
        # make camera behind fish looking at it from an angle
        self.camNP.setPosHpr(0, +10, 5, 180, -20, 0) 
        if index == self.userFishIndex:
            self.dirGUI.fishViewText.hide()
            self.dirGUI.userViewText.show()
        self.viewFoodButt.show()

    # clear all menus and gui elements for fishView mode
    def prepClearFishView(self):
        self.showAddMenu()
        self.dirGUI.topText.hide()
        self.dirGUI.topBack.hide()
        self.dirGUI.viewBack.hide()
        self.exitViewButt.hide()
        self.dirGUI.fishViewText.hide()
        self.dirGUI.userViewText.hide()
        self.viewFoodButt.hide()
        self.switchFront()
        # clear things needed for food
        self.dirGUI.foodBack.hide()
        self.dirGUI.foodpic.hide()
        self.grabFoodButt.hide()

    def clearFishView(self):
        self.prepClearFishView()
        for butt in self.viewButtList:
            butt.hide()
        self.fishViewing = False
        try:
            self.camNP.remove_node()
            sidesTex = loader.loadTexture("tex/blue.png")
            self.sides.setTexture(sidesTex)
            self.createFog()
            # self.displayRegion.setClearColor(VBase4(0,0,0,1))
            self.displayRegion.setClearColorActive(False)
            self.displayRegion.setClearDepthActive(False)
            self.displayRegion.setClearDepth(0)
            self.displayRegion = None
        except: pass



###
### USER FISH MODE

    def swimAsFish(self):
        self.hideAddMenu()
        self.makingUserFish = True # type is now userFish
        self.userFishButt.hide() # button to enter make own fish mode
        self.addFish2() # create this new fish
        self.haveUserFish = True




###
### CAMERA SHENANIGANS

    # move the camera up and rotate accordingly
    # don't move up beyond a certain point (200)
    def upCam(self):
        self.camDownButt.show() # button that allows shift camera down
        if self.camZ < 218:
            self.camZ += 10
            self.camP -= 4.44
            self.camY += 8.27778
            base.camera.setPosHpr(self.camX, self.camY, self.camZ, self.camH, 
                self.camP, self.camR)
        else: # can't move up any more! 
            self.camUpButt.hide() # no more up
            self.switchCamAer.hide() # can't switch to aerial mode
            self.switchCamFront.show() # switch cam to front view mode

    def downCam(self):
        self.camUpButt.show() # can hit camera up button
        if self.camZ > 38:
            self.camZ -= 10
            self.camY -= 8.27778
            self.camP += 4.44
            base.camera.setPosHpr(self.camX, self.camY, self.camZ, self.camH, 
                self.camP, self.camR)
        else: # too low!
            self.switchCamAer.show() # can go to aerial mode
            self.switchCamFront.hide() # can't go to front mode
            self.camDownButt.hide() # no more going down with camera

    # switch camera to aerial and hide certain buttons
    def switchAer(self):
        self.camX, self.camY, self.camZ = 0,-1,218
        self.camH, self.camP, self.camR = 0,-90,0
        base.camera.setPosHpr(self.camX, self.camY, self.camZ, self.camH, 
            self.camP, self.camR)
        self.switchCamAer.hide()
        self.switchCamFront.show()
        self.camDownButt.show()
        self.camUpButt.hide()

    def switchFront(self):
        self.camX, self.camY, self.camZ = 0,-150,38
        self.camH, self.camP, self.camR = 0,-10,0
        base.camera.setPosHpr(self.camX, self.camY, self.camZ, self.camH, 
            self.camP, self.camR)
        self.switchCamFront.hide()
        self.switchCamAer.show()
        self.camUpButt.show()
        self.camDownButt.hide()


### 
### FEED MODE
    def feedFish(self):
        # set a camera position for best feed fish viewing
        self.camX, self.camY, self.camZ = 0, -125.16666, 68
        self.camH, self.camP, self.camR = 0, -23.32, 0
        base.camera.setPosHpr(self.camX, self.camY, self.camZ, 
            self.camH, self.camP, self.camR)
        self.dirGUI.foodBack.show() # background
        self.dirGUI.foodpic.show()
        self.grabFoodButt.show()
    
    # can grab food multiple times
    def grabFood(self):
        self.grabFoodButt.hide()
        self.feedTask()

    # load flake model
    def feedTask(self):
        self.flakeX, self.flakeY, self.flakeZ = 0, 0, 30

        self.flake = self.loader.loadModel("models/flake_1.egg")
        flakeTex = loader.loadTexture("tex/flakecolor.jpg")
        self.flake.setTexture(flakeTex)
        self.flake.reparentTo(self.render2)
        self.flake.setScale(1)
        self.flake.setPos(self.flakeX, self.flakeY, self.flakeZ)

        # mouse task syntax from Panda3d manual
        self.mousing = True
        taskMgr.add(self.feeding, "Feeding")

    # mouse task syntax from Panda3d manual
    # click places food piece down
    def placePiece(self):
        if self.mousing:
            self.flakeList += [Flake(self.flake, self.flakeX, 
                self.flakeY, self.flakeZ)]
            for fish in self.fishList:
                fish.feed(self.flakeList)
            self.mousing = False
            self.grabFoodButt.show()


    # borrowed method and modified from Panda 3D's looking-and-gripping example
    # model program
    def feeding(self, task):
        # Check to make sure the mouse is readable
        if self.mousing:
            # make sure within bounds!
            self.accept("mouse1", self.placePiece)
        else:
            return Task.done
        if base.mouseWatcherNode.hasMouse():
            # get the mouse position as a LVector2. The values for each axis 
            # are from -1 to 1. The top-left is (-1,-1), 
            # the bottom right is (1,1)
            self.flakeX=base.mouseWatcherNode.getMouseX() * 50
            self.flakeY=base.mouseWatcherNode.getMouseY() * 30
            self.flake.setPos(self.flakeX, self.flakeY, self.flakeZ)
        return Task.cont






# make a flake
# keep in mind the beginning position
class Flake(fishTank):
    def __init__(self, flake, x, y, z):
        self.flkX, self.flkY, self.flkZ = x,y,z
        self.flake = flake
        self.move()
        self.counter = 0
        self.xInc = +.15

    # always falling, swaying back and forth along x-axis
    # make sure still existing and not eaten already
    def fall(self):
        if self.flake != None:
            self.flkZ -= .2
            self.counter += 1
            self.flkX += self.xInc
            if self.counter % 5 == 0:
                self.xInc = -self.xInc
            if self.flkZ < 0:
                self.seq.pause()
            try:
                self.flake.setPos(self.flkX, self.flkY, self.flkZ)
            except:
                self.seq.pause()
        else: self.seq.pause()

    # sequence of falling and swaying back and forth
    def move(self):
        self.seq = Sequence()
        self.seq.append(Func(self.fall))
        self.seq.append(Wait(.15))
        self.seq.loop()





# fish class for each instance of the fish
# need to specify what type, which position
# contains all the methods necessary for a Fish
# contains more than 1 fish needs, so it's the superclass of Fish
# instantiating this kind is the normal community fish
class Fish(fishTank):

###
### CREATING FISH
    def __init__(self, typeFish, tankDims, name, render):
        (self.tankScale, self.tankLength, self.tankWidth, 
            self.tankHeight) = tankDims
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

        self.chaseX, self.chaseY, self.chaseZ = None, None, None
        self.chasingFood = False

    def remove(self):
        self.fishR.remove_node()
        self.fishL.remove_node()
        self.fishFront.remove_node()



###
### FISH MOVEMENT
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
        self.fishFront.setPos((self.xPosition, self.yPosition, self.zPosition))
        self.fishL.show()

    def moveTailRight(self):
        self.checkBounds()
        self.yPosition += self.yChange
        self.xPosition += self.xChange
        self.zPosition += self.zChange

        self.fishL.hide()
        self.fishFront.hide()
        self.fishR.setPos((self.xPosition, self.yPosition, self.zPosition))
        self.fishFront.setPos((self.xPosition, self.yPosition, self.zPosition))
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



###
### ROTATING U/D/L/R
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

    # random fish turns after a set number of moving straights
    def leftRightFish(self, numm):
        self.fishTurn += 1
        # self.fishTurn sets how far the fish moves before turning
        if self.fishTurn < 3: 
            return
        else:
            self.fishTurn = 0
        self.userLeftRight(numm)

    # userLeftRight is /just/ the left/right rotation, without above
    # randomization
    # turning the fish 45 degrees each time. need to make sure to change
    # how much x and z changes according to the direction the fish is facing
    def userLeftRight(self, numm):
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

    def upDownFish(self, numm):
        if (not(numm == 0 and self.headingChange > -30) and not(numm == 1 and 
            self.headingChange < 30)):
            self.headingChange = 0
            self.zChange = 0
        self.userUpDownFish(numm)

    # move fish up or down
    # includes pointing nose of fish up or down, then "y" axis shift
    def userUpDownFish(self, numm):
        # restrict to 30 degree angle
        if numm == 0 and self.headingChange > -30: # moving up
            self.headingChange -= 30 # angle fish pointing up
            self.zChange += 1

        elif numm == 1 and self.headingChange < 30: # moving down
            self.headingChange += 30
            self.zChange -= 1

        # set the new rotation for each of the models
        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))



###
### BOUNDS CHECKING
    # keep the fish within the limits of the tank
    # up and down positions were easy because you move the fish down/up
    # repectively.
    # For avoiding the sides of the wall, you need to keep into account the 
    # present orientation of the fish to turn it the way 
    # it is already pointing.
    # Also need to avoid endless loops when turning away.
    def checkBounds(self):
        zLimit, zmargin = self.tankHeight*self.tankScale, 8
        xLimit, xymargin = self.tankScale*self.tankLength, 12

        if self.zPosition < zmargin - 1: # actual basically bottom is 4
            self.upDownFish(0) # make fish move up
            return True
        if self.zPosition > zLimit - 4: # actual basically top is 30
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
            if self.pitchChange < 270 and self.pitchChange != 0:
                self.leftRightFish(1)
            else: self.leftRightFish(0)
            return True

        return self.checkYLimit()

    # not enough space, but checking y limit!
    def checkYLimit(self):
        yLimit, xymargin = self.tankScale*self.tankWidth, 12
        zmargin = 8
        # hitting front wall
        if self.yPosition > yLimit - xymargin:
            if self.pitchChange >= 180 or self.pitchChange == 0:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
            return True

        # hitting back wall
        if self.yPosition < -yLimit + zmargin:
            if self.pitchChange < 180:
                self.leftRightFish(0)
            else: self.leftRightFish(1)
            return True
        return False



###
### CHASING
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

    # find where the fish is in relation to the other fish or object
    # can only change x,y, and z by 1
    def preChase(self):
        x,y,z = self.chaseX, self.chaseY, self.chaseZ
        self.xyChange = [0,0]
        # depending where the other fish, can only change one xy by one
        if x - self.xPosition > 3: self.xyChange[0] = +1
        elif x - self.xPosition < -3: self.xyChange[0] = -1
        else: self.xyChange[0] = 0

        if y - self.yPosition > 3: self.xyChange[1] = +1
        elif y - self.yPosition < -3: self.xyChange[1] = -1
        else: self.xyChange[1] = 0

        # can change both zChange and Position (up/down less complicated)
        # only 3 states: -30, 0, and 30 degrees. Though can only move
        # up and down 30 degrees at a time
        if z - self.zPosition > 3: 
            if self.headingChange > -30: self.headingChange -= 30
            if self.headingChange == -30: self.zChange = +1

        elif z - self.zPosition < -3: 
            if self.headingChange < 30: self.headingChange += 30
            if self.headingChange == 30: self.zChange = -1

        else: 
            self.headingChange = 0
            self.zChange = 0

    # chasing another fish or object
    # can only rotate max 45 degrees, or go up or down 30 degrees
    # first get the x and y changes needed to go towards an object
    # find the pitch (rotate around z axis) from the tempXY Changes.
    # Adjust pitch only by 45 degrees towards the needed pitch
    # find new XYChanges based on the pitch we can realistically achieve
    def chase(self):
        self.preChase()
        self.tempxyChange = [self.xyChange[0], self.xyChange[1]]
        # find the needed rotation for this xyChange to look realistic
        neededPitch = self.findPitchChange()

        # turning left
        if ((neededPitch - self.pitchChange > 0 and neededPitch - 
            self.pitchChange < 180) or (neededPitch-self.pitchChange < 0 and 
            neededPitch-self.pitchChange <= -180)):
            self.pitchChange = (self.pitchChange + 45) % 360
        # turning right
        if ((neededPitch - self.pitchChange < 0 and neededPitch - 
            self.pitchChange >= -180) or neededPitch - self.pitchChange > 0 
            and neededPitch-self.pitchChange > 180):
            self.pitchChange = (360 + self.pitchChange - 45)%360

        self.findXYChange()

        self.fishL.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishR.setHpr((self.pitchChange, self.headingChange, 0))
        self.fishFront.setHpr((self.pitchChange, self.headingChange, 0))



###
### MOVE SEQUENCE

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

    # general function for moving Up down left or right!
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

    # make the sequence for moving
    # combination of moving straight and all the crazy things UDLR does
    def move(self):
        if not self.isMoving:
            self.isMoving = True
            self.seq = Sequence()
            self.moveStraight()
            self.seq.append(Func(self.UDLRFish))
            self.seq.loop()



###
### FEEDING
    # if no current flakes, then not chasing original food anymore!
    # make sure no other flakes otherwise still chasing
    # if no more flakes at all, stop chasing food sequence, and go back
    # to original movements
    def noFlakes(self):
        self.chasingFood = False
        for flake in self.flakeList:
            if flake != None:
                self.chasingFood = True
        if not self.chasingFood:
            self.foodSeq.pause()
            self.move()

    def chaseFood(self):
        # find closest food particle
        minDist, self.closestFlake = None, None
        for i in range(len(self.flakeList)):
            flake = self.flakeList[i]
            if flake != None:
                fooddist = (((flake.flkX-self.xPosition)**2 + (flake.flkY-
                    self.yPosition)**2 +(flake.flkZ-self.zPosition)**2)**.5)
                if minDist == None or fooddist < minDist:
                    self.indexFlake = i
                    self.closestFlake = flake
                    minDist = fooddist
        # no more flakes?? go to helper function above!
        if self.closestFlake == None: self.noFlakes()
        else:
            if minDist <= 5:
                self.flakeList[self.indexFlake] = None
                self.closestFlake.flake.removeNode()
                self.chaseFood() # recall to find next min piece
            if self.closestFlake != None:
                self.chaseX, self.chaseY, self.chaseZ =(self.closestFlake.flkX,
                self.closestFlake.flkY, self.closestFlake.flkZ)
                self.chase()

    # different move sequence for chasing food
    # break up original move's sequence with UDLR
    # this time, chase for food inbetween full tail movements
    def feed(self, flakeList):
        self.flakeList = flakeList
        try:
            if self.seq.isPlaying():
                self.isMoving = False
                self.seq.pause()
        except: pass
        if not self.chasingFood:
            self.chasingFood = True
            self.foodSeq = Sequence()
            self.foodSeq.append(Func(self.chaseFood))
            self.foodSeq.append(Wait(.15))
            self.foodSeq.append(Func(self.moveTailCenter))
            self.foodSeq.append(Wait(.15))
            self.foodSeq.append(Func(self.moveTailLeft))
            self.foodSeq.append(Wait(.15))
            self.foodSeq.append(Func(self.chaseFood))
            self.foodSeq.append(Func(self.moveTailCenter))
            self.foodSeq.append(Wait(.15))
            self.foodSeq.append(Func(self.moveTailRight))
            self.foodSeq.loop()





# make aggressive fish
# subclass of the huge Fish class
# Changes: need to use some of superclasses' chase functions to follow
# another fish. However, this time for a creature that follows another fish
# that is continuously moving and has a behavior of its own (as opposed to a 
# food flake)
class AggressiveFish(Fish):
    def __init__(self, fishType, tankDims, fishList, name, render):
        Fish.__init__(self, fishType, tankDims, name, render)
        self.chaseList = fishList
        self.chasableFish = None

    # make sure not chasing themselves
    def __eq__(self, other):
        return (isinstance(other, Fish) and (self.xPosition == 
            other.xPosition) and (self.yPosition == other.yPosition) and
            (self.zPosition == other.zPosition) and (self.name == other.name))

    # helper for chasable below
    # switch speeds back to normal if not chasing anymore
    def notChasing(self):
        if (abs(self.xChange) == 2 or abs(self.yChange) == 2 or
                abs(self.zChange) == 2):
            self.xChange /= 2
            self.yChange /= 2
            self.zChange /= 2
        for fish in self.chaseList:
            if (abs(fish.xChange) == 2 or abs(fish.yChange) == 2 or
                abs(fish.zChange) == 2):
                fish.xChange /= 2
                fish.yChange /= 2
                fish.zChange /= 2

    # see if any fish are minDistance away, and the closest fish at that
    def chasable(self):
        minDistance = 30
        tinyDist, self.dist = 6, 30
        chasedFish = None
        for fish in self.chaseList:
            if fish != self:
                self.dist = (((fish.xPosition - self.xPosition)**2 + 
                    (fish.yPosition - self.yPosition)**2 + (fish.zPosition - 
                    self.zPosition)**2)**0.5)
                # closest fish that is within the minDistance required to chase
                # try to make the other fish go faster
                if self.dist < minDistance:
                    chasedFish = fish
                    minDistance = self.dist
        if minDistance < tinyDist and chasedFish != None:
            if (abs(chasedFish.xChange) != 2 and abs(chasedFish.yChange) != 2 
                and abs(chasedFish.zChange) != 2):
                chasedFish.xChange *= 2
                chasedFish.yChange *= 2
                chasedFish.zChange *= 2
        if chasedFish == None:
            self.notChasing()
        return chasedFish

    # change the way the Fish's x, y, and z change to follow the 
    # chasableFish
    def chaseFish(self):
        fish = self.chasableFish
        self.chaseX, self.chaseY = fish.xPosition, fish.yPosition
        self.chaseZ = fish.zPosition
        self.chase()

    def possChase(self):
        self.chasableFish = self.chasable()
        if self.chasableFish != None:
            self.xChange *= 2
            self.yChange *= 2
            self.zChange *= 2
            self.chaseFish()
        else:
            self.UDLRFish()

    def move(self):
        self.seq = Sequence()
        self.seq.append(Func(self.possChase))
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





class UserFish(Fish):
    def __init__(self, fishType, tankDims, name, render):
        Fish.__init__(self, fishType, tankDims, name, render)

    # don't want the fish to automatically go to flake
    # use user controls
    def feed(self, flakeList):
        pass

# basically keep moving straight
# keys control turning left/right and up/down
    def checkMove(self):
        self.accept("arrow_up", self.userUpDownFish, [0])
        self.accept("arrow_down", self.userUpDownFish, [1])
        self.accept("arrow_right", self.userLeftRight, [1])
        self.accept("arrow_left", self.userLeftRight, [0])
        # print("check the user things")

    # combination of previous move and moving straight
    # after each tail turn check if the user has clicked anything!
    def move(self):
        if not self.isMoving:
            print("this seq")
            self.isMoving = True
            self.seq = Sequence()
            self.seq.append(Wait(.15))
            self.seq.append(Func(self.moveTailCenter))
            self.seq.append(Func(self.checkMove))
            self.seq.append(Wait(.15))
            self.seq.append(Func(self.moveTailLeft))
            self.seq.append(Func(self.checkMove))
            self.seq.append(Wait(.15))
            self.seq.append(Func(self.moveTailCenter))
            self.seq.append(Func(self.checkMove))
            self.seq.append(Wait(.15))
            self.seq.append(Func(self.moveTailRight))
            self.seq.append(Func(self.checkMove))
            self.seq.loop()





# Suggestions from below from Panda3D
# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
tank = fishTank()  # Create an instance of our class
tank.run()  # Run the simulation






