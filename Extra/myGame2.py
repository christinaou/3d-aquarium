from direct.showbase.ShowBase import ShowBase
 
class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
        self.world = self.loader.loadModel("world.bam")
        self.world.reparentTo(self.render)
 
        self.player = self.loader.loadModel("alliedflanker.egg")
        self.player.setPos(50, 50, 50)
        self.player.setH(100)
        self.player.reparentTo(self.render)

app = MyApp()
app.run()