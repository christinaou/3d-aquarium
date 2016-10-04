# Christina Ou
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



class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        # This code puts the standard title and instruction text on screen
        # format borrowed
        self.title = OnscreenText(text="My Aquarium of One (for now)",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)
        self.info = OnscreenText(text="Mouse to move, ESP to escape", 
            parent=base.a2dTopLeft, scale=.06, pos=(0.06, -.08 * 1), 
            fg=(1, 1, 1, 1), shadow=(0, 0, 0, .5), align=TextNode.ALeft)
        
        # Set up key input, borrowed
        self.accept('escape', sys.exit)

        # can't figure out camera's starting position
        # base.disableMouse()  # Disable mouse-based camera-control
        # camera.setPos(-2, -10, 1)  # -x, -z, -y Position the camera
        # camera.setHpr(0, 0, 0)
        base.trackball.node().setPos(0, 30, -1) # starting position of the camera
        
        fish1 = fish(fishTank)

class fish(fishTank):

    def __init__(self, ShowBase):
        super().__init__(ShowBase)

        self.createFish()
        
        # start with just one model
        self.fishR.hide()
        self.fishFront.hide()

        # initialize how far the fish moves each time
        self.zPosition = -1
        self.xPosition = 0
        self.zChange = -1
        self.xChange = 0

        # initialize pitch move each time the fish turns
        self.pitchChange = 0
        # moving one fish and its tial
        self.moveTail()

    def createFish(self):
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

        # set limits for where the fish can travel
        self.xLimits = (-20, 20)
        self.yLimits = (-20, 20)
        self.zLimits = (-10, 20)



    def moveTailLeft(self):
        # increment the distance of the fish
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0
        self.fishR.hide()
        self.fishFront.hide()
        # fish is moving self.zPosition space
        self.fishL.setPos((self.xPosition, self.zPosition, 0))
        self.fishL.show()

    def moveTailRight(self):
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0
        self.fishL.hide()
        self.fishFront.hide()
        self.fishR.setPos((self.xPosition, self.zPosition, 0))
        self.fishR.show()

    def moveTailCenter(self):
        self.zPosition += self.zChange
        self.xPosition += self.xChange
        # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
        # self.zPosition > self.zLimits[1]):
        #     self.zPosition = 0        
        self.fishL.hide()
        self.fishR.hide()
        self.fishFront.setPos((self.xPosition, self.zPosition, 0))
        self.fishFront.show()

    # turning the fish 45 degrees each time. need to make sure to change
    # how much x and z changes according to the direction the fish is facing
    def turnFish(self):
        # want to turn right, do -45
        # self.pitchChange = (self.pitchChange+45)%360 # turn left
        self.pitchChange = (360 + self.pitchChange - 45)%360 # turn right
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
        self.fishL.setHpr((self.pitchChange, 0, 0))
        self.fishR.setHpr((self.pitchChange, 0, 0))
        self.fishFront.setHpr((self.pitchChange, 0, 0))

    def moveTail(self):
        seq = Sequence() # syntax for Sequence from Panda3D library and forums
        # seq.append(Wait(.2))
        # seq.append(Func(self.moveTailRight))
        seq.append(Wait(.2))
        seq.append(Func(self.moveTailCenter))
        seq.append(Wait(.2))
        seq.append(Func(self.moveTailLeft))
        seq.append(Wait(.2))
        seq.append(Func(self.moveTailCenter))
        seq.append(Wait(.2))
        seq.append(Func(self.moveTailRight))
        seq.append(Wait(.2))
        seq.append(Func(self.turnFish))
        # seq.append(Wait(.05))
        # seq.append(Func(self.moveTailCenter))
        # seq.append(Func(self.moveTailRight))
        seq.loop()





# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
demo = fishTank()  # Create an instance of our class
demo.run()  # Run the simulation


