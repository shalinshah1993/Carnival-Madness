from math import pi, sin, cos
from direct.showbase.Transitions import Transitions
from pandac.PandaModules import loadPrcFileData
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Filename, AmbientLight, DirectionalLight, PointLight, Spotlight
from panda3d.core import PandaNode,NodePath,Camera,TextNode, PerspectiveLens
from panda3d.core import Vec3, Vec4, BitMask32, VBase4, AudioSound, WindowProperties
from direct.interval.IntervalGlobal import Sequence, Parallel
from panda3d.core import Point3, CollisionPlane, Plane
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
import sys, random, webbrowser
from direct.gui.DirectGui import *
from pandac.PandaModules import CollisionHandlerQueue, CollisionNode, CollisionSphere, CollisionTraverser
#import direct.directbase.DirectStart 
from direct.showbase.RandomNumGen import * 
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from panda3d.ai import *
from panda3d.core import TransparencyAttrib
from direct.gui.OnscreenImage import OnscreenImage
 
ABOUT_US_TEXT = "THIS GAME HAS BEEN DEVELOPED WITH A LOT OF EFFORTS BY TEAM \n F@DU G@MERS. TEAM MEMBERS INCLUDE SHALIN SHAH AND HARDIK VIRANI.\nCONTACT INFO - {201101179/201101066} @webmail.daiict.ac.in\n ANY FEEDBACK ??"
START_BUT_TEXT = "PLAY"
EXIT_BUT_TEXT = "EXIT"
HELP_BUT_TEXT = "HELP"
OPTION_BUT_TEXT = "PREFERENCES"
CREDITS_BUT_TEXT = "ABOUT US"
FULLSCREEN_BUT_TEXT = "Full Screen"
FULLSCREEN_LABEL = "Enable or Disable Full Screen"
SOUND_LABEL = "Enable or Disable Audio"
AUDIO_BUT_TEXT = "Sound"
GAME_OVER_LABEL = "ERRRR! THE MONSTER JUST NAILED YOU.\nYOUR SCORE : "
RESOLUTION_LABEL = "Screen Resolution Size"
LIGHT_BUT_TEXT = "Lights"
LIGHTS_LABEL = "Toggle Lights"
BACK_BUT_TEXT = "<--- BACK"
EXIT_TEXT = "Are you sure you would like to exit the game? All your progress would be lost?"
SAMPLE_LINK = "https://www.github.com/shalinshah1993/Carnival-Madness"


########################HEALTH/POWER VALUE CHANGES
INCR_HEALTH = 0.05
DECR_HEALTH = 0.1
DECR_POWER = 0.1
 
########################GAME STATES
STATE_RESET = 1
STATE_STARTED = 2
STATE_PREFS = 3
STATE_GAME_OVER = 4
STATE_PAUSED = 5
STATE_SCORE = 6
STATE_EXIT = 7 
STATE_HELP = 8 
 
#######################HEALTH VALUES
#Total Health - 100
#Lollipop - +2 
#Mint - +2
#GhostMode - No Collisions Applicable
 
class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		#To show the FPS
		loadPrcFileData('','show-frame-rate-meter 1')
		#Set background Image
		imageObject = OnscreenImage(parent = render2dp, image = 'models/heart.png', pos = (0.51, 0, 0.8), scale = (0.05, 0.07, 0.07))
		imageObject.setTransparency(TransparencyAttrib.MAlpha)
		imageObject = OnscreenImage(parent = render2dp, image = 'models/speed.png', pos = (0.51, 0, 0.6), scale = (0.05, 0.07, 0.09))
		imageObject.setTransparency(TransparencyAttrib.MAlpha)
		imageObject1 = OnscreenImage(parent = render2dp, image = 'models/face.png', pos = (-0.3, 0, 0.8), scale = (0.07, 0.1, 0.1))
		imageObject1.setTransparency(TransparencyAttrib.MAlpha)
		OnscreenText(text = 'X', pos = (-1.45, 0.75), scale = 0.09, fg =( 1, 1, 0, 1), bg = (0.1,0.1,0.1, 1))
		imageObject2 = OnscreenImage(parent = render2dp, image = 'models/lollipop.png', pos = (-0.9, 0, 0.8), scale = (0.07, 0.1, 0.1))
		imageObject2.setTransparency(TransparencyAttrib.MAlpha)
		OnscreenText(text = 'X', pos = (-0.35, 0.75), scale = 0.09, fg =( 1, 1, 0, 1), bg = (0.1,0.1,0.1, 1))
		
		#base.cam2dp.node().getDisplayRegion(0).setSort(-20)
		#Disable Camera change by mouse and hide mouse pointer, Set Full creen
		base.disableMouse()
		
		self.keyMap = {"left":0, "right":0, "forward":0, "back":0}
		self.worldView = False
		self.hasJet = False
		self.nearCarousel = False
		self.nearOctopus = False
		self.nearSkyride = False
		self.nearTent = False
		self.nearHouse = False
		self.nearCoaster = False
		self.nearLollipop = False
		self.nearMint = False
		self.nearMonster = False
		self.lights = False
		self.pose = False
		self.nearBridge = False
		self.enableAudio = True
		self.screenResolutionVal = 4
		self.isFullScreen = False
		self.hasStarted = False
		self.hasResumed = False
		self.hasBoost = False
		self.hasGhostPower = False
		self.curState = STATE_RESET
	
		#These instance field shows health of character
		self.boyHealth = 100
		self.boostCount = 100
		self.curScore = 0
		self.noOfLives = 2
		
		#Load all the necessary sounds for the game
		self.themeSong = self.loader.loadMusic('audio/game.wav')
		self.hauntedHouseSong = self.loader.loadSfx("audio/horror.ogg")
		self.butHoverSound = self.loader.loadSfx("audio/but_hover.wav")
		self.collectSound = self.loader.loadSfx("audio/collect.wav")
		self.mintCollectSound = self.loader.loadSfx("audio/capsule.wav")
		self.lifeDownSound = self.loader.loadSfx("audio/gameOver.wav")
		self.boyHurtSound = self.loader.loadSfx("audio/boyHurt.wav")
		self.peopleScream = self.loader.loadSfx("audio/scream.wav")
		self.themeSong.setVolume(0.4)
		self.collectSound.setVolume(1.0)
		self.hauntedHouseSong.setVolume(1.0)
		self.mintCollectSound.setVolume(1.0)
		self.lifeDownSound.setVolume(1.0)
		self.boyHurtSound.setVolume(1.0)
		
		#Load all the Models and Actors
		self.loadAllModels()
		
		######------>
		self.AIworld = AIWorld(self.render)
		self.AIchar = AICharacter("boy",self.monster, 150, 5, 150)
		self.AIworld.addAiChar(self.AIchar)
		self.AIbehaviors = self.AIchar.getAiBehaviors()
		self.AIbehaviors.pursue(self.boy,1.0) 
		self.monster.loop("run")
		
		#Set up the Collision Nodes 
		self.setupCollisionNodes()
		
		#Set initial Camera Distance from Ralph
		self.y = 30
		self.z = 13		
		
		#Start all the animations in the environment
		self.animatethings()
		
		#Add the task to move boy and rotate camera to get world View
		self.taskMgr.add(self.boyMoveTask, "BoyMoveTask")
		self.taskMgr.add(self.cameraLightCollisionTask, "cameraLightCollisionTask")
		
		#Write all the methods to be done when you press a key!
		self.accept("arrow_left", self.keys, ["left",1] )
		self.accept("arrow_right", self.keys, ["right",1])
		self.accept("arrow_up",self.keys, ["forward",1])
		self.accept("arrow_up-up",self.keys, ["forward", 0])
		self.accept("arrow_left-up",self.keys, ["left",0])
		self.accept("arrow_right-up",self.keys, ["right", 0])
		self.accept("e",self.switchToJet)
		self.accept("escape", self.switchState, [STATE_STARTED, STATE_PAUSED])
		self.accept("l",self.changeLights)
		self.accept("wheel_up",self.keys, ["wheel_up",1])
		self.accept("wheel_down", self.keys, ["wheel_down",1])
		
		#Turn on ambient and directional Light for better graphics
		self.ambientLight = AmbientLight("ambientLight")
		self.ambientLight.setColor(Vec4(1, 1, 1, 1))
		self.sunLight = PointLight('plight')
		self.sunLight.setColor(VBase4(3, 3, 3, 1))
		self.sLight = self.render.attachNewNode(self.sunLight)
		self.sLight.setPos(350,300,150)
		
		#self.directionalLight = DirectionalLight("directionalLight")
		#self.directionalLight.setDirection(Vec3(-5, -5, -5))
		#self.directionalLight.setColor(Vec4(1, 1, 1, 1))
		#self.directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
		#self.dLight = self.render.attachNewNode(self.directionalLight)
		self.aLight = self.render.attachNewNode(self.ambientLight);
		self.hutLight = self.tent.attachNewNode(PointLight('tentLight'))
		self.hutLight.setPos(0,0,120)
		
		#Turn on the light effects and set world view for background of GUI
		#self.switchView()
		self.changeLights()
		
	def animatethings(self):
		
		seq1 = self.hawk.posInterval(4, Point3(250, 250, 50))
		seq3 = self.hawk.posInterval(4, Point3(-250, 250, 50))
		seq2 = self.hawk.hprInterval(0.1, Point3(80, 0, 0), startHpr = Point3(50, 0, 0))
		seq4 = self.hawk.hprInterval(0.1, Point3(70, 0, 0), startHpr = Point3(120, 0, 0))
		seq5 = self.hawk.posInterval(2, Point3(-100, 250, 30))
		seq6 = self.hawk.hprInterval(0.1, Point3(80, 0, 0), startHpr = Point3(50, 0, 0))
		seq7 = self.hawk.posInterval(4, Point3(250, 20, 20))
		seq8 = self.hawk.hprInterval(0.1, Point3(70, 0, 0), startHpr = Point3(120, 0, 0))
		seq9 = self.hawk.posInterval(4, Point3(0, 0, 100))
		seq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9)
		seq.loop()
		
		seq1 = self.hawk1.posInterval(4, Point3(-100, 50, 50))
		seq3 = self.hawk1.posInterval(4, Point3(-50, 250, 50))
		seq2 = self.hawk1.hprInterval(0.1, Point3(30, 0, 0), startHpr = Point3(50, 0, 0))
		seq4 = self.hawk1.hprInterval(0.1, Point3(90, 0, 0), startHpr = Point3(120, 0, 0))
		seq5 = self.hawk1.posInterval(2, Point3(-200, 150, 50))
		seq6 = self.hawk1.hprInterval(0.1, Point3(60, 0, 0), startHpr = Point3(50, 0, 0))
		seq7 = self.hawk1.posInterval(4, Point3(200, 200, 50))
		seq8 = self.hawk1.hprInterval(0.1, Point3(190, 0, 0), startHpr = Point3(120, 0, 0))
		seq9 = self.hawk1.posInterval(4, Point3(200, 0, 100))
		seq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9)
		seq.loop()
		
		seq1 = self.flamingo.posInterval(6, Point3(30, 70, 0))
		seq3 = self.flamingo.posInterval(2, Point3(70, 80, 0))
		seq2 = self.flamingo.hprInterval(2, Point3(-90, 0, 0), startHpr = Point3(0, 0, 0))
		seq4 = self.flamingo.hprInterval(0.1, Point3(-180, 0, 0), startHpr = Point3(-90, 0, 0))
		seq5 = self.flamingo.posInterval(2, Point3( 60, 50, 0))
		seq6 = self.flamingo.hprInterval(0.1, Point3(-270, 0, 0), startHpr = Point3(-180, 0, 0))
		seq7 = self.flamingo.posInterval(4, Point3(15, 50, 0))
		seq8 = self.flamingo.hprInterval(1, Point3( -180, 0, 0), startHpr = Point3(-270, 0, 0))
		seq9 = self.flamingo.posInterval(4, Point3(15, -10,0))
		seq10 = self.flamingo.hprInterval(1, Point3(-90, 0, 0), startHpr = Point3(-180, 0, 0))
		seq11 = self.flamingo.posInterval(4, Point3(30, -10, 0))
		seq12 = self.flamingo.hprInterval(1, Point3(0, 0, 0), startHpr = Point3(-90, 0, 0))
		seq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9, seq10, seq11, seq12)
		seq.loop()
		
		seq1 = self.blueBird.posInterval(8, Point3(-250, 200, 50))
		seq3 = self.blueBird.posInterval(8, Point3(-250, -200, 50))
		seq2 = self.blueBird.hprInterval(1, Point3(50, 0, 0), startHpr = Point3(0, 0, 0))
		seq4 = self.blueBird.hprInterval(1, Point3(30, 0, 0), startHpr = Point3(50, 0, 0))
		seq5 = self.blueBird.posInterval(5, Point3(-200, 150, 50))
		seq6 = self.blueBird.hprInterval(1, Point3(60, 0, 0), startHpr = Point3(50, 0, 0))
		seq7 = self.blueBird.posInterval(4, Point3(200, 200, 50))
		seq8 = self.blueBird.hprInterval(1, Point3(190, 0, 0), startHpr = Point3(120, 0, 0))
		seq9 = self.blueBird.posInterval(5, Point3(200, 0, 100))
		seq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9)
		seq.loop()
		
		seq1 = self.Dropship.posInterval(5, Point3(-130, -120, 40))
		seq2 = self.Dropship.posInterval(6, Point3(-130, 70, 40))
		seq3 = self.Dropship.posInterval(5, Point3(-130, 130, 13))
		seq4 = self.Dropship.hprInterval(3, Point3( 180, 0, 0), startHpr = Point3(0, 0, 0))
		seq5 = self.Dropship.posInterval(5, Point3(-130, 70, 40))
		seq6 = self.Dropship.posInterval(6, Point3(-130, -120, 40))
		seq7 = self.Dropship.posInterval(5, Point3(-130, -160, 13))
		seq8 = self.Dropship.hprInterval(3, Point3( 180, 0, 0), startHpr = Point3(0, 0, 0))
		self.skyRideSeq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8)
		self.skyRideSeq.loop()
	
	def changeLights(self):
		if self.lights == False:
			self.render.setLight(self.aLight)
			self.render.setLight(self.sLight)
			#self.render.setLight(self.dLight)
			self.lights = True
		else:
			self.render.clearLight(self.aLight)
			self.render.clearLight(self.sLight)
			#self.render.clearLight(self.dLight)
			self.lights = False
		
	def climbOnJet(self):
		x = self.boy.getX(); y = self.boy.getY(); 
		x1 = self.jets.getX(); y1 = self.jets.getY(); 
		if self.hasJet:
			seq1 = self.boy.posInterval(1, Point3( x, y, 10))
			seq2 = self.jets.posInterval(1, Point3( 0, 0, 0))
			seq = Parallel(seq1, seq2)
			seq.start()
		else:
			seq1 = self.boy.posInterval(0.05, Point3( x, y, 15))
			par1 = self.boy.posInterval(0.5, Point3( x, y, 0))
			par2 = self.jets.posInterval(0.5, Point3( 0, -800, 350))
			seq = Sequence(seq1)
			seq.start()
			par = Parallel(par1, par2)
			par.start()
		return		
	      
	def switchToJet(self):
		if self.hasJet:
		      self.hasJet = False
		      self.climbOnJet()
		else:
		      self.jets.setScale(0.4)
		      self.hasJet = True
		      self.climbOnJet()
		return
	      
	def switchView(self):
		if self.worldView:
			taskMgr.remove("SpinCameraTask")
			self.worldView = False
			self.hasStarted = True
			self.hasResumed = True
			props = WindowProperties()
			props.setCursorHidden(True) 
			base.win.requestProperties(props)
			self.ambientLight.setColor(Vec4(.3, .3, .3, 1))
			#self.directionalLight.setDirection(Vec3(-5, -5, -5))
			
			self.startBut.hide(); self.exitBut.hide(); self.optionsBut.hide(); self.aboutBut.hide()
			self.transit.letterboxOff(2.5)
		else:
			taskMgr.add(self.spinCameraTask, "SpinCameraTask")
			self.worldView = True
			self.hasStarted = False
			self.hasResumed = False
			props = WindowProperties()
			props.setCursorHidden(False) 
			base.win.requestProperties(props)
			self.ambientLight.setColor(Vec4(.1, .1, .1, 1))
			#self.directionalLight.setDirection(Vec3( 5, 5, 5))	
			
			self.startBut.show(); self.exitBut.show(); self.optionsBut.show(); self.aboutBut.show()
			self.transit.letterboxOn(2.5)
			#Transitions(loader).fadeScreenColor(LVecBase4f(0.1,0.1,0.1,1))

	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.camera.setPos(320 * sin(angleRadians), -320.0 * cos(angleRadians), 30)
		self.camera.setHpr(angleDegrees, 0, 0)
		return Task.cont
	      
	def keys(self,action,args):
		#print action,args
	    #If camera goes away then Y should change faster while if it comes near then Z should change faster
		if action == "wheel_down":
			self.y = self.y - 2.5
			self.z = self.z - 5
			if self.y < 30:
				self.y = 30
			if self.z < 13:
				self.z = 13
		elif action == "wheel_up":
			self.y = self.y + 5
			self.z = self.z + 2
			if self.y > 160:
				self.y = 160
			if self.z > 50:
				self.z = 50
		if action == "forward":
			self.keyMap["forward"] = args
		if action == "right":
			self.keyMap["right"] = args
		if action == "left":
			self.keyMap["left"] = args
	      
	def cameraLightCollisionTask(self,task):
		base.camera.setPos(self.boy.getX(),self.boy.getY() - self.y, self.z)
		
		angleDegrees = task.time * 1.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.sky.setHpr(angleDegrees, 0, 0)

		#Checks if we are near any of the rides inorder to create spatial awareness
		carouselDist = (self.boy.getPos() - self.carousel.getPos()).length()
		if carouselDist < 150:
				self.nearCarousel = True
		else:
				self.nearCarousel = False
		octopusDist = (self.boy.getPos() - self.octopus.getPos()).length()
		if octopusDist < 150:
				self.nearOctopus = True
		else:
				self.nearOctopus = False
		tentDist = (self.boy.getPos() - self.tent.getPos()).length()
		if tentDist < 150:
				self.nearTent = True
		else:
				self.nearTent = False
		skyRideDist = (self.boy.getPos() - self.skyRide.getPos()).length()
		if skyRideDist < 150:
				self.nearSkyride = True
		else:
				self.nearSkyride = False
		coasterDist = (self.boy.getPos() - self.coaster.getPos()).length()
		if coasterDist < 150:
				self.nearCoaster = True
		else:
				self.nearCoaster = False
		monsterDist = (self.boy.getPos() - self.monster.getPos()).length()
		if monsterDist < 17:
				self.nearMonster = True
		else:
				self.nearMonster = False
		
		if base.mouseWatcherNode.hasMouse() and self.curState == STATE_STARTED:
			base.camera.setH(-90 * base.mouseWatcherNode.getMouseX())
			base.camera.setP(45* base.mouseWatcherNode.getMouseY())
			#base.camera.lookAt(self.boy)
			#self.camera.setX(base.camera, -20 * globalClock.getDt())
		if self.enableAudio:
			if not self.themeSong.status() == self.themeSong.PLAYING:
				self.sfxManagerList[0].update()
				self.themeSong.play()
		#if self.song.status() == AudioSound.BAD:
		#	print "BAD"
		#elif self.song.status() == AudioSound.READY:
		#	print "READY"
		#else:
		#	print "PLAYING"
		
		if self.curState == STATE_STARTED:
			if self.nearCarousel:
				angleDegrees = task.time * 12.0
				angleRadians = angleDegrees * (pi / 180.0)
				self.carousel.setHpr(angleDegrees, 0, 0)
			if self.nearOctopus:
				angleDegrees = task.time * 12.0
				angleRadians = angleDegrees * (pi / 180.0)
				self.octopus.setHpr(angleDegrees, 0, 0)
			if self.nearTent:
				self.tent.setLight(self.hutLight)
			else:
				self.tent.clearLight(self.hutLight)
			if self.nearSkyride:
				self.skyRideSeq.pause()
			else:
				if not self.skyRideSeq.isPlaying():
					self.skyRideSeq.resume()
			if self.nearHouse:
				if not self.hauntedHouseSong.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.hauntedHouseSong.play()
					self.sfxManagerList[0].update()
			else:
				if self.hauntedHouseSong.status() == self.hauntedHouseSong.PLAYING:
					self.hauntedHouseSong.stop()
			if self.nearLollipop:
				if not self.collectSound.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.collectSound.play()
					self.sfxManagerList[0].update()
			if not self.nearBridge:
				self.boy.setZ(0)
			if self.nearMonster:
				self.boyHealth -= 2
				self.healthBar['value'] = self.boyHealth
				if not self.boyHurtSound.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.boyHurtSound.play()
					self.sfxManagerList[0].update()
			else:
				if self.boyHurtSound.status() == self.hauntedHouseSong.PLAYING:
					self.boyHurtSound.stop()
			if self.nearMint:
				if not self.mintCollectSound.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.mintCollectSound.play()
					self.sfxManagerList[0].update()
			if self.nearCoaster:
				if not self.peopleScream.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.peopleScream.play()
					self.sfxManagerList[0].update()
			else:
				if self.peopleScream.status() == self.hauntedHouseSong.PLAYING:
					self.peopleScream.stop()
					
		self.cTrav.traverse(render)
		self.collisionHandler1.sortEntries()
		if self.collisionHandler1.getNumEntries() == 0:
			self.startPos = self.boy.getPos()
			# self.nearCarousel = False
			# self.nearOctopus = False
			# self.nearSkyride = False
			# self.nearTent = False
			# self.nearHouse = False
			# #self.pose = False
			self.nearBridge = False
			self.nearLollipop = False
			self.nearMint = False
			self.nearMonster = False
			self.nearElixir = False
		else:
			#self.nearBridge = False
			for i in range(self.collisionHandler1.getNumEntries()):
				entry = self.collisionHandler1.getEntry(i).getIntoNodePath().getName()
				#print entry
				# if "cCarouselNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					# self.nearCarousel = True
				# elif "cOctopusNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					# self.nearOctopus = True
				# elif "cTentNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					# self.nearTent = True
				# elif "cSkyrideNode1" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName() or "cSkyrideNode2" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					# self.nearSkyride = True
				# elif "cHouseNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					# self.nearHouse = True
					
				x = random.randint(-350,350)
				y = random.randint(-350,350)
				z = random.randint(0,1)
				if "cLollipop" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					self.lollipop[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].hide()
					self.lollipop[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].setPos(x,y,0)
					self.lollipop[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].show()
					self.curScore += 1
					self.boyHealth = (self.boyHealth + 5)
					#self.countLabel[str(self.curScore)]
					self.countLabel["text"] = str(self.curScore)
					if self.boyHealth > 100:
						self.boyHealth = 100
						self.healthBar['value'] = 100
					else:
						self.healthBar['value'] += 5 
					self.nearLollipop = True
				if "cMint" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					self.mint[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].hide()
					self.lollipop[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].setPos(x,y,0)
					self.lollipop[int(self.collisionHandler1.getEntry(i).getIntoNodePath().getTag('key'))].show()
					self.boyHealth = 100
					self.healthBar['value'] = 100
					self.nearMint = True
				if "bridge" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					self.boy.setZ(self.collisionHandler1.getEntry(i).getSurfacePoint(self.render)[2] - 2.5)
					self.nearBridge = True

				if "cHeadNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					if self.boyHealth > 10:
					      self.boyHealth -= 2
					else:
					      self.boyHealth = 0
					self.healthBar['value'] = self.boyHealth
					self.nearMonster = True
				if "cBottleNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					self.boostCount = 100
					self.powerBar['value'] = 100
					self.hasBoost = True
					self.cBoy.hide()
					self.hasGhostPower = False
				if "cCandleNode" == self.collisionHandler1.getEntry(i).getIntoNodePath().getName():
					self.powerBar['value'] = 100
					self.cBoy.show()
					self.hasGhostPower = True
					self.hasBoost = False
			
			if not self.hasGhostPower:
				if not (self.nearBridge or self.nearLollipop or self.nearMint):
					self.boy.setPos(self.startPos)
		return Task.cont
		
###This method is used to change the health of actor which gets tired by running.
	def health(self):
		if self.isMoving:
			# self.countMonster=self.countMonster+1
			self.boyHealth = self.boyHealth - DECR_HEALTH
			self.healthBar['value'] -= DECR_HEALTH
			if self.boostCount > 0: 
				self.boostCount = self.boostCount - DECR_POWER
				self.powerBar['value'] -= DECR_POWER
			if self.boostCount < 0 or self.boostCount == 0:
				self.boostCount = 0
				self.powerBar['value'] = 0
				if self.hasGhostPower:
					self.hasGhostPower = False
					self.cBoy.hide()
				if self.hasBoost:
					self.hasBoost = False
		else:
			if self.boyHealth < 100:
				self.boyHealth = self.boyHealth + INCR_HEALTH
				self.healthBar['value'] += INCR_HEALTH
			if self.boostCount > 0: 
				self.boostCount = self.boostCount - DECR_POWER
				self.powerBar['value'] -= DECR_POWER
			if self.boostCount < 0 or self.boostCount == 0:
				self.boostCount = 0
				self.powerBar['value'] = 0
				if self.hasGhostPower:
					self.hasGhostPower = False
					self.cBoy.hide()
				if self.hasBoost:
					self.hasBoost = False

		if self.boostCount == 0:
			self.hasBoost = False
		
		if (self.boyHealth < 0 or self.boyHealth == 0):
			if not self.lifeDownSound.status() == AudioSound.PLAYING:
					if self.enableAudio:
						self.lifeDownSound.play()
					self.sfxManagerList[0].update()
					
			if self.noOfLives == 0:
				self.switchState(STATE_STARTED, STATE_GAME_OVER)
			else:
				self.noOfLives -= 1
				self.boyHealth = 100
				self.healthBar['value'] = 100
				self.lifeLabel["text"] = str(self.noOfLives)
		# if (self.countMonster == 0):
			# seq1 = self.monster.posInterval(2, Point3(0, 2, 5))
			# seq1.start()
			# self.monster.loop("run")
			# textObject = OnscreenText(text = 'Game Over Monster Killed You!!!', pos = (0, 0.50), scale = 0.1)
			# #self.switchView()
			#self.switchView()		
			
		# if (self.countMonster > 100):
			# seq1 = self.monster.posInterval(2, Point3(0, 20, 5))
			# seq1.start() 		
			
#These are the methods to move Ralph from his position as per the arrow keys
	def boyMoveTask(self, task):
		if self.curState == STATE_STARTED:
			self.health()
			if not self.hasBoost or self.hasGhostPower:
				if self.keyMap["forward"] != 0:
					self.boy.setY(self.boy, -35 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["left"] != 0:
					self.boy.setH(self.boy.getH() + 300 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["right"] != 0:
					self.boy.setH(self.boy.getH() - 300 * globalClock.getDt())
					self.isMoving = True
			elif self.hasBoost and not self.hasGhostPower:
				if self.keyMap["forward"] != 0:
					self.boy.setY(self.boy, -65 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["left"] != 0:
					self.boy.setH(self.boy.getH() + 525 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["right"] != 0:
					self.boy.setH(self.boy.getH() - 525 * globalClock.getDt())
					self.isMoving = True
			else:
				if self.keyMap["forward"] != 0:
					self.boy.setY(self.boy, -35 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["left"] != 0:
					self.boy.setH(self.boy.getH() + 300 * globalClock.getDt())
					self.isMoving = True
				if self.keyMap["right"] != 0:
					self.boy.setH(self.boy.getH() - 300 * globalClock.getDt())
					self.isMoving = True
			if not (self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"]):
				self.isMoving = False
			if self.isMoving:
				if not self.myAnimControl.isPlaying():
					self.boy.loop("run")
			else:
				self.boy.pose("walk", 5)
			
			#self.AIbehaviors.pursue(self.boy, 1.0)
			self.AIworld.update()
			self.monster.setZ(15)
			#if self.isMoving and not self.hasJet:
			#	if not self.myAnimControl.isPlaying():
			#		self.boy.loop("run")
				#self.AIbehaviors.addToPath(self.boy.getPos())
				#self.AIbehaviors.startFollow()
		#	if not self.isMoving:
		#		if self.rotateBack:
		#			self.boy.setH(self.boy.getH() + 10)
		#			if self.boy.getH() % 180 == 0:
		#				self.rotateBack = False
		#		elif self.rotateRight:
		#			self.boy.setH(self.boy.getH() + 10)
		#			if self.boy.getH() % 180 == 0:
		#				self.rotateRight = False
		#		elif self.rotateLeft:
		#			self.boy.setH(self.boy.getH() - 10)
		#			if self.boy.getH() % 180 == 0:
		#				self.rotateLeft = False
				#else:
				#	self.boy.pose("walk", 5)
			#self.health()
		return Task.again	
		
	def keyUp(self):
		self.boy.setY(self.boy, -35 * globalClock.getDt())
		#self.boy.setY(self.boy.getY() + 2)
		self.isMoving = True
		#####------>
		#self.health()
	
	def keyDown(self):
		if not self.rotateBack:
			self.boy.setH(self.boy.getH() + 10)
			#base.camera.setH(self.boy.getH()+10)
			if self.boy.getH() % 180 == 0:
				self.rotateBack = True
		else:
			self.boy.setY(self.boy.getY() - 2)
			self.isMoving = True
			#####------>
			#self.health()
		
	def stopWalk(self):
		self.isMoving = False
		#####------>
		#self.health()
	
	def keyLeft(self):
		self.boy.setH(self.boy.getH() + 300 * globalClock.getDt())
		#if not self.rotateLeft:
		#	self.boy.setH(self.boy.getH() + 10)
		#	if self.boy.getH() % 90 == 0:
		#		self.rotateLeft = True
		#else:
		#	self.boy.setX(self.boy.getX() - 2)
		#	self.isMoving = True
			#####------>
		#	#self.health()
		
	def keyRight(self):
		self.boy.setH(self.boy.getH() - 300 * globalClock.getDt())
		#if not self.rotateRight:
		#	self.boy.setH(self.boy.getH() - 10)
		#	if self.boy.getH() % 90 == 0:
		#		self.rotateRight = True
		#else:
		#	self.boy.setX(self.boy.getX() + 2)
		#	self.isMoving = True
		#	#####------>
		#	#self.health()
	
	def hideMainMenu(self):
		self.startBut.hide()
		self.optionsBut.hide()
		self.exitBut.hide()
		self.aboutBut.hide()
		self.helpBut.hide()
		
	def showMainMenu(self):
		self.startBut.show()
		self.optionsBut.show()
		self.exitBut.show()
		self.aboutBut.show()
		self.helpBut.show()
		
	def showPrefs(self):
		self.labelFullScreen.show()
		self.labelSound.show()
		self.fullScreenBut.show()
		self.backBut.show()
		self.audioBut.show()
		self.labelLights.show()
		self.lightsBut.show()
	
	def hidePrefs(self):
		self.labelFullScreen.hide()
		self.labelSound.hide()
		self.fullScreenBut.hide()
		self.audioBut.hide()
		self.backBut.hide()
		self.showMainMenu()
		self.labelLights.hide()
		self.lightsBut.hide()
		
	def hideHelpMenu(self):
		self.lollipopCard.hide()
		self.lollipopCard1.hide()
		self.lifeCard.hide()
		self.lifeCard1.hide()
		self.staminaCard.hide()
		self.staminaCard1.hide()
		self.boostCard.hide()
		self.boostCard1.hide()
		self.backBut2.hide()
	
	def showHelpMenu(self):
		self.lollipopCard.show()
		self.lollipopCard1.show()
		self.lifeCard.show()
		self.lifeCard1.show()
		self.staminaCard.show()
		self.staminaCard1.show()
		self.boostCard.show()
		self.boostCard1.show()
		self.backBut2.show()
		
	def hideGameOverMenu(self):
		self.playAgainBut.hide()
		self.submitScore.hide()
		self.submitBut.hide()
		self.backBut1.hide()
		self.gameOverLabel.hide()
	
	def showGameOverMenu(self):
		self.playAgainBut.show()
		self.submitScore.show()
		self.submitBut.show()
		self.backBut1.show()
		self.gameOverLabel.show()
	
	def toggleLights(self,status):
		self.changeLights()
		
	def setResolution(self):
		if self.resolutionSlider['value']/25 == 4:
			self.screenResolutionVal = 4
			self.labelLights1['text'] = "Screen Resolution :- 1600 * 900"
		elif self.resolutionSlider['value']/25 == 3:
			self.screenResolutionVal = 3
			self.labelLights1['text'] = "Screen Resolution :- 1366 * 768"
		elif self.resolutionSlider['value']/25 == 2:
			self.screenResolutionVal = 2
			self.labelLights1['text'] = "Screen Resolution :- 1024 * 768"
		elif self.resolutionSlider['value']/25 == 1:
			self.screenResolutionVal = 1
			self.labelLights1['text'] = "Screen Resolution :- 800 * 600"
	
	def toggleScreen(self,status):
		props = WindowProperties()
		if not status:
			self.isFullScreen = False
			props.setFullscreen(False)
		else:
			self.isFullScreen = True
			props.setSize(1366, 768)
			props.setFullscreen(True)
		base.win.requestProperties(props)
		
	def toggleAudio(self,status):
		if not status:
			self.enableAudio = False
			if self.themeSong.status() == self.themeSong.PLAYING:
				self.themeSong.stop()
		else:
			self.enableAudio = True
			
	def setupCollisionNodes(self):
		#Collision Nodes are created here and attached to spheres
		self.cBoy = self.boy.attachNewNode(CollisionNode('cBoyNode'))
		self.cBoy.node().addSolid(CollisionSphere(0, 0, 3, 2.5))
		self.cStall = self.stall.attachNewNode(CollisionNode('cStallNode'))
		self.cStall.node().addSolid(CollisionSphere(0, 0, 0, 1.5))
		self.cBottle = self.elixir.attachNewNode(CollisionNode('cBottleNode'))
		self.cBottle.node().addSolid(CollisionSphere(0, 0, 0, 1))
		self.cCandle = self.candle.attachNewNode(CollisionNode('cCandleNode'))
		self.cCandle.node().addSolid(CollisionSphere(0, 0, 0, 50))
		self.cHead1 = self.blueHead.attachNewNode(CollisionNode('cHeadNode'))
		self.cHead1.node().addSolid(CollisionSphere(0, 0, 0, 8))
		self.cHead2 = self.blueHead1.attachNewNode(CollisionNode('cHeadNode'))
		self.cHead2.node().addSolid(CollisionSphere(0, 0, 0, 8))
		self.cHead3 = self.blueHead2.attachNewNode(CollisionNode('cHeadNode'))
		self.cHead3.node().addSolid(CollisionSphere(0, 0, 0, 8))
		self.cHead4 = self.blueHead3.attachNewNode(CollisionNode('cHeadNode'))
		self.cHead4.node().addSolid(CollisionSphere(0, 0, 0, 8))
		#self.cMonster = self.monster.attachNewNode(CollisionNode('cMonsterNode'))
		#self.cMonster.node().addSolid(CollisionSphere(0, 0, 0, 3))
		#self.cHouse = self.house.attachNewNode(CollisionNode('cHouseNode'))
		#self.cHouse.node().addSolid(CollisionSphere(0, 0, 0, 200))
		#self.cCarousel = self.carousel.attachNewNode(CollisionNode('cCarouselNode'))
		#self.cCarousel.node().addSolid(CollisionSphere(0, 0, 0, 30))
		#self.cOctopus = self.octopus.attachNewNode(CollisionNode('cOctopusNode'))
		#self.cOctopus.node().addSolid(CollisionSphere(0, 0, 0, 65))
		#self.cTent = self.tent.attachNewNode(CollisionNode('cTentNode'))
		#self.cTent.node().addSolid(CollisionSphere(0, 0, 0, 65))
		#self.cCoaster = self.coaster.attachNewNode(CollisionNode('cCoasterNode'))
		#self.cCoaster.node().addSolid(CollisionSphere(0, 0, 0, 170))
		self.cBridge = self.bridge.attachNewNode(CollisionNode('cBridge'))
		self.cBridge.node().addSolid(CollisionSphere(0, 0, 0, 25))
		self.cRingtoss = self.ringToss.attachNewNode(CollisionNode('cRingtoss'))
		self.cRingtoss.node().addSolid(CollisionSphere(0, 0, 0, 100))
		
		self.cSkyride1 = self.skyRide.attachNewNode(CollisionNode('cSkyrideNode1'))
		self.cSkyride1.node().addSolid(CollisionSphere(0, -250, 0, 40))
		
		self.cSkyride2 = self.skyRide.attachNewNode(CollisionNode('cSkyrideNode2'))
		self.cSkyride2.node().addSolid(CollisionSphere(0, 250, 0, 40))
		
		self.cPond = self.pGround.attachNewNode(CollisionNode('cPond'))
		self.cPond.node().addSolid(CollisionSphere(-100, 0, 0, 40))
		self.cPond1 = self.pGround.attachNewNode(CollisionNode('cPond1'))
		self.cPond1.node().addSolid(CollisionSphere(-220, -170, 0, 120))
		self.cPond2 = self.pGround.attachNewNode(CollisionNode('cPond2'))
		self.cPond2.node().addSolid(CollisionSphere(-15, -10, 0, 50))
		self.cPond3 = self.pGround.attachNewNode(CollisionNode('cPond3'))
		self.cPond3.node().addSolid(CollisionSphere(-15, 80, 0, 50))
		
		self.cFence = self.fence.attachNewNode(CollisionNode('cFence'))
		self.cFence.node().addSolid(CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, 0, 0))))
		self.cFence1 = self.fence1.attachNewNode(CollisionNode('cFence1'))
		self.cFence1.node().addSolid(CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 0, 0))))
		self.cFence2 = self.fence2.attachNewNode(CollisionNode('cFence2'))
		self.cFence2.node().addSolid(CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, 0, 0))))
		self.cFence3 = self.fence3.attachNewNode(CollisionNode('cFence3'))
		self.cFence3.node().addSolid(CollisionPlane(Plane(Vec3(0, -1, 0), Point3(0, 0, 0))))
		
		lollipopCollisionNodes = []
		for i in xrange(15):
			collisionNode = self.lollipop[i].attachNewNode(CollisionNode('cLollipop'))
			collisionNode.node().addSolid(CollisionSphere(0, 0, 0, 0.5))
			collisionNode.setTag('key', str(i))
			lollipopCollisionNodes.append(collisionNode)
			
		mintCollisionNodes = []
		for i in xrange(10):
			collisionNode = self.mint[i].attachNewNode(CollisionNode('cMint'))
			collisionNode.node().addSolid(CollisionSphere(0, 0, 0, 0.5))
			collisionNode.setTag('key', str(i))
			mintCollisionNodes.append(collisionNode)
		
		#Uncomment this lines to see the collision spheres
		#self.cStall.show()
		#self.cHouse.show()
		#self.cCarousel.show()
		#self.cBoy.show()
		#self.cMonster.show()
		#self.cOctopus.show()
		#self.cCoaster.show()
		#self.cPond.show()
		#self.cPond1.show()
		#self.cPond2.show()
		#self.cPond3.show()
		#self.cFence.show()
		#self.cFence1.show()
		#self.cFence2.show()
		#self.cFence3.show()
		#self.cRingtoss.show()
		#self.cTent.show()
		#self.cSkyride1.show()
		#self.cSkyride2.show()
		#self.cBottle.show()
		#self.cCandle.show()
		#self.cHead1.show()
		#self.cHead2.show()
		#self.cHead3.show()
		#self.cHead4.show()
		
		self.cTrav=CollisionTraverser()
		self.collisionHandler1 = CollisionHandlerQueue()
		self.cTrav.addCollider(self.cBoy, self.collisionHandler1)
		
	def aboutUs(self, args):
		print args
		if args == 1:
			webbrowser.open(SAMPLE_LINK)
		self.aboutUsDialog.cleanup()
		
	def quit(self, args):
		if args:
			taskMgr.doMethodLater(2.6 ,sys.exit,'Exiting')
			self.transit.irisOut(2.5)
		self.askDialog.cleanup()
	
	def load2dObjects(self):
		text = TextNode('Lollipop')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("1. This indicates the number of Lollipop's you've collected! Collect more to score more")
		self.lollipopCard = aspect2d.attachNewNode(text)
		self.lollipopCard.setScale(0.07)
		self.lollipopCard.setPos(-1.3,0,0.5)
		
		text = TextNode('Lollipop')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("01.")
		self.lollipopCard1 = aspect2d.attachNewNode(text)
		self.lollipopCard1.setScale(0.07)
		self.lollipopCard1.setPos(-1.7,0,0.73)
		
		text = TextNode('Life')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("2. This indicates the number of lives.You start with three lives.")
		self.lifeCard = aspect2d.attachNewNode(text)
		self.lifeCard.setScale(0.07)
		self.lifeCard.setPos(-0.7,0,0.2)
		
		text = TextNode('Life')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("02.")
		self.lifeCard1 = aspect2d.attachNewNode(text)
		self.lifeCard1.setScale(0.07)
		self.lifeCard1.setPos(-0.72,0,0.73)
		
		text = TextNode('Health')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("3. This indicates your weariness or stamina level. More you run more you become tired,less would be this value")
		self.staminaCard = aspect2d.attachNewNode(text)
		self.staminaCard.setScale(0.07)
		self.staminaCard.setPos(0.3,0,0)
		
		text = TextNode('Health')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("03.")
		self.staminaCard1 = aspect2d.attachNewNode(text)
		self.staminaCard1.setScale(0.07)
		self.staminaCard1.setPos(0.75,0,0.73)
		
		text = TextNode('Boost')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("4. This indicates the amount of boost you've got. Its limited! You can collect more by picking up elixir or candle which you can find in map")
		self.boostCard = aspect2d.attachNewNode(text)
		self.boostCard.setScale(0.07)
		self.boostCard.setPos(1 ,0, -0.4)
		
		text = TextNode('Boost')
		text.setSmallCaps(True)
		text.setWordwrap(15.0)
		text.setAlign(TextNode.ACenter)
		text.setFrameColor(1, 1, 1, 1)
		text.setCardColor(1, 1, 0.5, 1)
		text.setCardDecal(True)
		text.setTextColor(0, 0, 0, 1)
		text.setCardAsMargin(0, 0, 0, 0)
		text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
		text.setText("04.")
		self.boostCard1 = aspect2d.attachNewNode(text)
		self.boostCard1.setScale(0.07)
		self.boostCard1.setPos(0.75 ,0, 0.56)
	
		self.healthBar = DirectWaitBar(text = "", value = 100, range = 100, pos = (1.35,0.4,0.8), barColor = (1, 0, 0, 1), scale = 0.4)
		self.powerBar = DirectWaitBar(text = "", value = 0, range = 100, pos = (1.35,0.4,0.6), barColor = (0, 1 , 0, 1), scale = 0.4)
		self.countLabel = DirectLabel(text = str(self.curScore), scale = 0.2, pos = (-1.25 , 0, 0.75))
		self.lifeLabel = DirectLabel(text = str(self.noOfLives), scale = 0.2, pos = (-0.2 , 0, 0.75))
	
	def loadAllModels(self):
		#FadeIn the First Time when app starts
		self.transit = Transitions(loader)
		self.transit.irisIn(2.5)
		taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		props = WindowProperties()
		props.setCursorHidden(False) 
		base.win.requestProperties(props)
		self.transit.letterboxOn(2.5)
		
		#All the actors, models are loaded here 
		self.pGround = self.loader.loadModel("models/ParkGround")
		self.pGround.reparentTo(self.render)
		self.pGround.setPos(0,0,0)
		self.pGround.setScale(0.5,0.53,0.25)#(0.30, 0.30, 0.25)
		self.pGround.setHpr(180,0,0)
		
		self.fence = self.loader.loadModel("models/fence")
		self.fence.reparentTo(self.render)
		self.fence.setPos(355,-10,0)
		self.fence.setScale(55, 3, 2)
		self.fence.setHpr(90,0,0)
		self.fence1 = self.loader.loadModel("models/fence")
		self.fence1.reparentTo(self.render)
		self.fence1.setPos(-355,-10,0)
		self.fence1.setScale(55, 3, 2)
		self.fence1.setHpr(90,0,0)
		self.fence2 = self.loader.loadModel("models/fence")
		self.fence2.reparentTo(self.render)
		self.fence2.setPos(0,330,0)
		self.fence2.setScale(55, 3, 2)
		self.fence2.setHpr(180,0,0)
		self.fence3 = self.loader.loadModel("models/fence")
		self.fence3.reparentTo(self.render)
		self.fence3.setPos(180,-330,0)
		self.fence3.setScale(26, 3, 2)
		self.fence3.setHpr(180,0,0)
		self.fence4 = self.loader.loadModel("models/fence")
		self.fence4.reparentTo(self.render)
		self.fence4.setPos(-180,-330,0)
		self.fence4.setScale(26, 3, 2)
		self.fence4.setHpr(180,0,0)		
		
		self.gate = self.loader.loadModel("models/gate")
		self.gate.reparentTo(self.render)
		self.gate.setPos(0,-325,-5)
		self.gate.setScale(0.01, 0.02, 0.01)
		self.gate.setHpr(180,0,0)
		
		self.coaster = self.loader.loadModel("models/Coaster")
		self.coaster.reparentTo(self.render)
		self.coaster.setScale(0.3, 0.5, 0.5)
		self.coaster.setPos(-290, 50, 0)
		self.coaster.setHpr(270,0,0)
		
		self.fWheel = self.loader.loadModel("models/FerrisWheel")
		self.fWheel.reparentTo(self.render)
		self.fWheel.setScale(2.5, 2, 2)
		self.fWheel.setPos(310, -10, 1)
		self.fWheel.setHpr(100,0,0)
		
		self.tent = self.loader.loadModel("models/tent")
		self.tent.reparentTo(self.render)
		self.tent.setScale(1.2, 1.2, 0.9)
		self.tent.setPos(280, 260, 0)
		self.tent.setHpr(150,0,0)
		
		self.bridge = self.loader.loadModel("models/bridge")
		self.bridge.reparentTo(self.render)
		self.bridge.setPos(32,17,15)
		self.bridge.setHpr(90,0,0)
		self.bridge.setScale(0.15,0.05,0.05)
		
		self.carousel = self.loader.loadModel("models/Carousel")
		self.carousel.reparentTo(self.render)
		self.carousel.setScale(3, 3, 2)
		self.carousel.setPos(270, -270, 2)
		self.carousel.setHpr(180,0,0)
		
		self.smiley = self.loader.loadModel("models/smiley")
		self.smiley.reparentTo(self.carousel)
		self.smiley.setScale(2, 2, 2)
		self.smiley.setHpr(180, 0, 0)
		self.smiley.setPos(0, 0, 18)
		
		self.octopus = self.loader.loadModel("models/Octopus")
		self.octopus.reparentTo(self.render)
		self.octopus.setScale(1,1,1.5)
		self.octopus.setPos(-260,-270,1)
		self.octopus.setHpr(320,0,0)

		self.house = self.loader.loadModel("models/HauntedHouse")
		self.house.reparentTo(self.render)
		self.house.setScale(0.8, 0.6, 1.6)
		self.house.setPos(60,260,1)
		self.house.setHpr(180,0,0)
		
		self.stall = self.loader.loadModel("models/popcorncart")
		self.stall.reparentTo(self.render)
		self.stall.setScale(6,6,3)
		self.stall.setPos(-40,-180,6)
		self.stall.setHpr(0,0,0)
		
		self.stallMan = self.loader.loadModel("models/Man")
		self.stallMan.reparentTo(self.render)
		self.stallMan.setScale(2.2,3.0,2.2)
		self.stallMan.setPos(-45,-180,0)
		self.stallMan.setHpr(-90,0,0)
		
		self.stallWoman = self.loader.loadModel("models/Mana")
		self.stallWoman.reparentTo(self.render)
		self.stallWoman.setScale(2.5)
		self.stallWoman.setPos(-34,-180,0)
		self.stallWoman.setHpr(90,0,0)
		
		self.stallGuy = self.loader.loadModel("models/RandomGuy")
		self.stallGuy.reparentTo(self.render)
		self.stallGuy.setScale(-2.2,3.0,2.2)
		self.stallGuy.setPos(-34,-175,0)
		self.stallGuy.setHpr(90,0,0)
		
		self.boymodel = Actor("models/boymodel",{"dance":"models/boyanimation"})
		self.boymodel.reparentTo(self.render)
		self.boymodel.setScale(0.015)
		self.boymodel.setPos(-42, -180, 14)
		self.boymodel.setHpr(-60,20,0)
		self.boymodel.loop('dance')
		
		self.hawk = self.loader.loadModel("models/hawk")
		self.hawk.reparentTo(self.render)
		self.hawk.setScale(2,2,1)
		self.hawk.setPos(0, 0, 100)		
		self.hawk1 = self.loader.loadModel("models/hawk")
		self.hawk1.reparentTo(self.render)
		self.hawk1.setScale(2,2,1)
		self.hawk1.setPos(200, 0, 100)
		
		self.Shrubbery = self.loader.loadModel("models/Shrubbery")
		self.Shrubbery.reparentTo(self.render)
		self.Shrubbery.setScale(0.01, 0.04, 0.01)
		self.Shrubbery.setPos(-28, 10, 0)
		self.Shrubbery.setHpr(0,0,0)
		self.Shrubbery1 = self.loader.loadModel("models/Shrubbery")
		self.Shrubbery1.reparentTo(self.render)
		self.Shrubbery1.setScale(0.01, 0.04, 0.01)
		self.Shrubbery1.setPos(-26, 30, 0)
		self.Shrubbery1.setHpr(0,0,0)
		self.Shrubbery2 = self.loader.loadModel("models/Shrubbery")
		self.Shrubbery2.reparentTo(self.render)
		self.Shrubbery2.setScale(0.01, 0.04, 0.01)
		self.Shrubbery2.setPos(-24, 20, 0)
		self.Shrubbery2.setHpr(0,0,0)
		self.Shrubbery3 = self.loader.loadModel("models/Shrubbery")
		self.Shrubbery3.reparentTo(self.render)
		self.Shrubbery3.setScale(0.01, 0.04, 0.01)
		self.Shrubbery3.setPos(60, 20, 0)
		self.Shrubbery3.setHpr(0,0,0)
		
		self.palmtree = self.loader.loadModel("models/palmtree")
		self.palmtree.reparentTo(self.render)
		self.palmtree.setScale(3, 3, 3)
		self.palmtree.setPos(-30, -60, 0)
		self.palmtree.setHpr(0,0,0)
		self.palmtree1 = self.loader.loadModel("models/palmtree")
		self.palmtree1.reparentTo(self.render)
		self.palmtree1.setScale(3, 3, 3)
		self.palmtree1.setPos(-55, -105, 0)
		self.palmtree2 = self.loader.loadModel("models/palmtree")
		self.palmtree2.reparentTo(self.render)
		self.palmtree2.setScale(3, 3, 3)
		self.palmtree2.setPos(-80, -70, 0)
		self.palmtree3 = self.loader.loadModel("models/palmtree")
		self.palmtree3.reparentTo(self.render)
		self.palmtree3.setScale(3, 3, 3)
		self.palmtree3.setPos(-60, -35, 0)
		self.palmtree4 = self.loader.loadModel("models/palmtree")
		self.palmtree4.reparentTo(self.render)
		self.palmtree4.setScale(3, 3, 3)
		self.palmtree4.setPos(-30, -30, 0)
		self.palmtree5 = self.loader.loadModel("models/palmtree")
		self.palmtree5.reparentTo(self.render)
		self.palmtree5.setScale(3, 3, 3)
		self.palmtree5.setPos(-30, -90, 0)
		
		self.palmtree6 = self.loader.loadModel("models/palmtree")
		self.palmtree6.reparentTo(self.render)
		self.palmtree6.setScale(3, 3, 3)
		self.palmtree6.setPos(-15, -300, 0)
		self.palmtree6.setHpr(0,0,0)
		self.palmtree7 = self.loader.loadModel("models/palmtree")
		self.palmtree7.reparentTo(self.render)
		self.palmtree7.setScale(3, 3, 3)
		self.palmtree7.setPos(-15, -310, 0)
		self.palmtree8 = self.loader.loadModel("models/palmtree")
		self.palmtree8.reparentTo(self.render)
		self.palmtree8.setScale(3, 3, 3)
		self.palmtree8.setPos(-15, -290, 0)
		self.palmtree9 = self.loader.loadModel("models/palmtree")
		self.palmtree9.reparentTo(self.render)
		self.palmtree9.setScale(3, 3, 3)
		self.palmtree9.setPos(15, -290, 0)
		self.palmtree10 = self.loader.loadModel("models/palmtree")
		self.palmtree10.reparentTo(self.render)
		self.palmtree10.setScale(3, 3, 3)
		self.palmtree10.setPos(15, -300, 0)
		self.palmtree11 = self.loader.loadModel("models/palmtree")
		self.palmtree11.reparentTo(self.render)
		self.palmtree11.setScale(3, 3, 3)
		self.palmtree11.setPos(15, -310, 0)
		
		self.palmtree12 = self.loader.loadModel("models/palmtree")
		self.palmtree12.reparentTo(self.render)
		self.palmtree12.setScale(3, 3, 3)
		self.palmtree12.setPos(-15, -320, 0)
		self.palmtree13 = self.loader.loadModel("models/palmtree")
		self.palmtree13.reparentTo(self.render)
		self.palmtree13.setScale(3, 3, 3)
		self.palmtree13.setPos(15, -280, 0)
		self.palmtree14 = self.loader.loadModel("models/palmtree")
		self.palmtree14.reparentTo(self.render)
		self.palmtree14.setScale(3, 3, 3)
		self.palmtree14.setPos(15, -270, 0)
		self.palmtree15 = self.loader.loadModel("models/palmtree")
		self.palmtree15.reparentTo(self.render)
		self.palmtree15.setScale(3, 3, 3)
		self.palmtree15.setPos(15, -320, 0)
		self.palmtree17 = self.loader.loadModel("models/palmtree")
		self.palmtree17.reparentTo(self.render)
		self.palmtree17.setScale(3, 3, 3)
		self.palmtree17.setPos(-15, -280, 0)
		self.palmtree17.setHpr(0,0,0)
		self.palmtree16 = self.loader.loadModel("models/palmtree")
		self.palmtree16.reparentTo(self.render)
		self.palmtree16.setScale(3, 3, 3)
		self.palmtree16.setPos(-15, -270, 0)
		
		self.pineTree = self.loader.loadModel("models/Pine_tree")
		self.pineTree.setScale(0.1)
		self.pineTree.reparentTo(self.render)
		self.pineTree.setPos(100, -160, 15)
		
		self.HappyTree = self.loader.loadModel("models/HappyTree")
		self.HappyTree.setScale(0.1)
		self.HappyTree.reparentTo(self.render)
		self.HappyTree.setPos(50, -100, 10)
		self.HappyTree.setHpr(10,0,0)
		
		self.HappyTree1 = self.loader.loadModel("models/HappyTree")
		self.HappyTree1.setScale(0.1)
		self.HappyTree1.reparentTo(self.render)
		self.HappyTree1.setPos(10, -110, 10)
		self.HappyTree1.setHpr(10,0,0)
		
		self.HappyTree2 = self.loader.loadModel("models/HappyTree")
		self.HappyTree2.setScale(0.1)
		self.HappyTree2.reparentTo(self.render)
		self.HappyTree2.setPos(180, -80, 10)
		self.HappyTree2.setHpr(100,0,0)
		
		self.HappyTree3 = self.loader.loadModel("models/HappyTree")
		self.HappyTree3.setScale(0.1)
		self.HappyTree3.reparentTo(self.render)
		self.HappyTree3.setPos(10, 140, 10)
		self.HappyTree3.setHpr(10,0,0)
		
		self.HappyTree4 = self.loader.loadModel("models/HappyTree")
		self.HappyTree4.setScale(0.1)
		self.HappyTree4.reparentTo(self.render)
		self.HappyTree4.setPos(50, 140, 10)
		self.HappyTree4.setHpr(100,0,0)
		
		self.flamingo = self.loader.loadModel("models/flamingo")
		self.flamingo.reparentTo(self.render)
		self.flamingo.setScale(0.1, 0.1, 0.1)
		self.flamingo.setPos(30, -10, 1)
		self.flamingo.setHpr(0,0,0)
		
		self.lampPost = self.loader.loadModel("models/LampPost")
		self.lampPost.reparentTo(self.render)
		self.lampPost.setScale(2, 2, 2)
		self.lampPost.setPos(40, -185, 0)
		self.lampPost.setHpr(-30,0,0)
		self.text = TextNode('Lollipop')
		
		self.lampPost1 = self.loader.loadModel("models/LampPost")
		self.lampPost1.reparentTo(self.render)
		self.lampPost1.setScale(2, 2, 2)
		self.lampPost1.setPos(25, -140, 0)
		self.lampPost1.setHpr(150,0,0)
		self.lampPost2 = self.loader.loadModel("models/LampPost")
		self.lampPost2.reparentTo(self.render)
		self.lampPost2.setScale(2, 2, 2)
		self.lampPost2.setPos(-10, -154, 0)
		self.lampPost2.setHpr(217,0,0)
		self.lampPost3 = self.loader.loadModel("models/LampPost")
		self.lampPost3.reparentTo(self.render)
		self.lampPost3.setScale(2, 2, 2)
		self.lampPost3.setPos(-10, -185, 0)
		self.lampPost3.setHpr(40,0,0)
		#self.lampPost.find("**/cLamp").node().setIntoCollideMask(BitMask32.bit(0))
		
		self.Pyramid = self.loader.loadModel("models/Pyramid")
		self.Pyramid.reparentTo(self.render)
		self.Pyramid.setScale(0.2)
		self.Pyramid.setPos(-280, 240, 0)
		self.Pyramid.setHpr(0,0,0)
		
		self.Sphinx = self.loader.loadModel("models/Sphinx")
		self.Sphinx.reparentTo(self.render)
		self.Sphinx.setScale(0.04)
		self.Sphinx.setPos(-230, 240, 8)
		self.Sphinx.setHpr(180,0,0)
		
		self.Sphinx1 = self.loader.loadModel("models/Sphinx")
		self.Sphinx1.reparentTo(self.render)
		self.Sphinx1.setScale(0.04)
		self.Sphinx1.setPos(-280, 190, 8)
		self.Sphinx1.setHpr(-90,0,0)
		
		self.blueHead = Actor("models/head",{"attack":"models/head-hurt"})
		self.blueHead.reparentTo(self.render)
		self.blueHead.setScale(2)
		self.blueHead.setPos(-210, 250, 15)
		self.blueHead.setHpr(0,0,0)
		self.blueHead.loop('attack')
		seq1 = self.blueHead.posInterval(4, Point3(-210, 180, 15))
		seq2 = self.blueHead.posInterval(4, Point3(-210, 250, 15))
		self.blueHeadseq = Sequence(seq1, seq2)
		self.blueHeadseq.loop()
		
		self.blueHead1 = Actor("models/head",{"attack":"models/head-hurt"})
		self.blueHead1.reparentTo(self.render)
		self.blueHead1.setScale(2)
		self.blueHead1.setPos(-270, 180, 15)
		self.blueHead1.setHpr(0,0,0)
		self.blueHead1.loop('attack')
		seq3 = self.blueHead1.posInterval(4, Point3(-270, 130, 15))
		seq4 = self.blueHead1.posInterval(4, Point3(-270, 180, 15))
		self.blueHeadseq1 = Sequence(seq3, seq4)
		self.blueHeadseq1.loop()
		
		self.blueHead2 = Actor("models/head",{"attack":"models/head-hurt"})
		self.blueHead2.reparentTo(self.render)
		self.blueHead2.setScale(2)
		self.blueHead2.setPos(70, -115, 15)
		self.blueHead2.setHpr(-90,0,0)
		self.blueHead2.loop('attack')
		seq5 = self.blueHead2.posInterval(2, Point3(0, -120, 15))
		seq6 = self.blueHead2.posInterval(2, Point3(70, -115, 15))
		self.blueHeadseq2 = Sequence(seq5, seq6)
		self.blueHeadseq2.loop()
		
		self.blueHead3 = Actor("models/head",{"attack":"models/head-hurt"})
		self.blueHead3.reparentTo(self.render)
		self.blueHead3.setScale(2)
		self.blueHead3.setPos(0, 140, 15)
		self.blueHead3.setHpr(90,0,0)
		self.blueHead3.loop('attack')
		seq6 = self.blueHead3.posInterval(2, Point3(70, 140, 15))
		seq7 = self.blueHead3.posInterval(2, Point3(0, 140, 15))
		self.blueHeadseq3 = Sequence(seq6, seq7)
		self.blueHeadseq3.loop()
		
		
		self.ringToss = self.loader.loadModel("models/ringtoss")
		self.ringToss.reparentTo(self.render)
		self.ringToss.setScale(0.3,0.3,0.5)
		self.ringToss.setPos(-270, -85, 0)
		self.ringToss.setHpr(90,0,0)
		
		self.RandomGuy = self.loader.loadModel("models/RandomGuy")
		self.RandomGuy.reparentTo(self.render)
		self.RandomGuy.setScale(2.5)
		self.RandomGuy.setPos(-235, -65, 0)
		self.RandomGuy.setHpr(180,0,0)
		
		self.RandomGirl1 = self.loader.loadModel("models/RandomGirl1")
		self.RandomGirl1.reparentTo(self.render)
		self.RandomGirl1.setScale(2.5)
		self.RandomGirl1.setPos(-235, -75, 0)
		self.RandomGirl1.setHpr(0,0,0)
		
		self.RandomGirl2 = self.loader.loadModel("models/RandomGirl2")
		self.RandomGirl2.reparentTo(self.render)
		self.RandomGirl2.setScale(2.5)
		self.RandomGirl2.setPos(-235, -85, 0)
		self.RandomGirl2.setHpr(180,0,0)
		
		self.RandomGirl3 = self.loader.loadModel("models/RandomGirl3")
		self.RandomGirl3.reparentTo(self.render)
		self.RandomGirl3.setScale(2.5)
		self.RandomGirl3.setPos(-235, -95, 0)
		self.RandomGirl3.setHpr(0,0,0)
		
		self.Kelly = self.loader.loadModel("models/Kelly")
		self.Kelly.reparentTo(self.render)
		self.Kelly.setScale(2.5)
		self.Kelly.setPos(-15, -155, 0)
		self.Kelly.setHpr(180,0,0)
		
		self.skyRide = self.loader.loadModel("models/Skyride")
		self.skyRide.reparentTo(self.render)
		self.skyRide.setScale(0.7,0.6,0.9)
		self.skyRide.setPos(-130, -20, 0)
		self.skyRide.setHpr(0,0,0)
		
		self.Dropship = self.loader.loadModel("models/Dropship")
		self.Dropship.reparentTo(self.render)
		self.Dropship.setScale(0.3)
		self.Dropship.setPos(-130, -160, 13)
		self.Dropship.setHpr(0,0,0)
		
		# self.MtFuji = self.loader.loadModel("models/MtFuji")
		# self.MtFuji.reparentTo(self.render)
		# self.MtFuji.setScale(0.3)
		# self.MtFuji.setPos(450, 550, -20)
		# self.MtFuji.setHpr(0,0,0)
		self.MtFuji1 = self.loader.loadModel("models/MtFuji")
		self.MtFuji1.reparentTo(self.render)
		self.MtFuji1.setScale(0.3)
		self.MtFuji1.setPos(-650, 550, -20)
		self.MtFuji1.setHpr(0,0,0)
		self.MtFuji2 = self.loader.loadModel("models/MtFuji")
		self.MtFuji2.reparentTo(self.render)
		self.MtFuji2.setScale(0.3)
		self.MtFuji2.setPos(0, 750, -20)
		self.MtFuji2.setHpr(0,0,0)
		self.MtFuji3 = self.loader.loadModel("models/MtFuji")
		self.MtFuji3.reparentTo(self.render)
		self.MtFuji3.setScale(0.3)
		self.MtFuji3.setPos(450, 750, -20)
		self.MtFuji3.setHpr(0,0,0)
		self.volcano = self.loader.loadModel("models/hill")
		self.volcano.reparentTo(self.render)
		self.volcano.setScale(1)
		self.volcano.setPos(250, 700, -20)
		self.volcano.setHpr(0,0,0)
		self.volcano1 = self.loader.loadModel("models/hill")
		self.volcano1.reparentTo(self.render)
		self.volcano1.setScale(1)
		self.volcano1.setPos(-600, 250, -20)
		self.volcano1.setHpr(0,0,0)
		self.volcano2 = self.loader.loadModel("models/hill")
		self.volcano2.reparentTo(self.render)
		self.volcano2.setScale(1)
		self.volcano2.setPos(-250, 700, -20)
		self.volcano2.setHpr(0,0,0)
		self.volcano3 = self.loader.loadModel("models/hill")
		self.volcano3.reparentTo(self.render)
		self.volcano3.setScale(1)
		self.volcano3.setPos(-450, 700, -20)
		self.volcano3.setHpr(0,0,0)
		self.volcano4 = self.loader.loadModel("models/hill")
		self.volcano4.reparentTo(self.render)
		self.volcano4.setScale(1)
		self.volcano4.setPos(550, 250, -20)
		self.volcano4.setHpr(-90,0,0)
		self.volcano5 = self.loader.loadModel("models/hill")
		self.volcano5.reparentTo(self.render)
		self.volcano5.setScale(1)
		self.volcano5.setPos(-650, -150, -20)
		self.volcano5.setHpr(0,0,0)
		self.volcano6 = self.loader.loadModel("models/hill")
		self.volcano6.reparentTo(self.render)
		self.volcano6.setScale(1)
		self.volcano6.setPos(700, -250, -20)
		self.volcano6.setHpr(0,0,0)
		
		self.blueBird = self.loader.loadModel("models/bluebird")
		self.blueBird.reparentTo(self.render)
		self.blueBird.setScale(4)
		self.blueBird.setPos(200, 0, 100)	
		self.blueBird1 = self.loader.loadModel("models/bluebird")
		self.blueBird1.reparentTo(self.blueBird)
		self.blueBird1.setScale(1)
		self.blueBird1.setPos(3, -1, 0)
		self.blueBird2 = self.loader.loadModel("models/bluebird")
		self.blueBird2.reparentTo(self.blueBird)
		self.blueBird2.setScale(1)
		self.blueBird2.setPos(3, 1, 0)
		self.blueBird3 = self.loader.loadModel("models/bluebird")
		self.blueBird3.reparentTo(self.blueBird)
		self.blueBird3.setScale(1)
		self.blueBird3.setPos(6, -1, 0)
		self.blueBird4 = self.loader.loadModel("models/bluebird")
		self.blueBird4.reparentTo(self.blueBird)
		self.blueBird4.setScale(1)
		self.blueBird4.setPos(6, 1, 0)
		
		############
		self.sun = Actor("models/sun",{"shine":"models/sunrotate"})
		self.sun.reparentTo(self.render)
		self.sun.setScale(0.2)
		self.sun.setPos(350, 350, 150)
		self.sun.setHpr(90,0,0)
		self.sun.loop('shine')
		
		self.sky = self.loader.loadModel("models/skysphere")
		self.sky.reparentTo(self.render)
		self.sky.setScale(5)
		self.sky.setPos(0, 0, -30)
		self.sky.setHpr( -180, 0, 0)
		
		self.elephant = Actor("models/elephantmodel",{"fly":"models/elephantanimation"})
		self.elephant.reparentTo(self.render)
		self.elephant.setScale(0.3)
		self.elephant.setPos(50, 180, 100)
		self.elephant.setHpr(-60,20,0)
		self.elephant.loop('fly')
		seq1 = self.elephant.posInterval(40, Point3(-100, 250, 100))
		seq3 = self.elephant.posInterval(40, Point3(250, 200, 100))
		seq5 = self.elephant.posInterval(40, Point3(-200, 250, 100))
		seq9 = self.elephant.posInterval(40, Point3(50, 180, 100))
		seq = Sequence(seq1, seq3, seq5, seq9)
		seq.loop()
		
		self.gw01 = Actor("models/gw01",{"gw02":"models/gw02","gw03":"models/gw03","gw04":"models/gw04","gw05":"models/gw05","gw06":"models/gw06","gw07":"models/gw07","gw08":"models/gw08"})
		self.gw01.reparentTo(self.render)
		self.gw01.setScale(0.04)
		self.gw01.setPos(265, 180, 14)
		self.gw01.setHpr(-60,0,0)
		self.gw01.loop('gw02')
		self.gw01.loop('gw03')
		self.gw01.loop('gw04')
		self.gw01.loop('gw05')
		self.gw01.loop('gw06')
		self.gw01.loop('gw07')
		self.gw01.loop('gw08')
		self.bw01 = Actor("models/bw01",{"bw02":"models/bw02","bw03":"models/bw03"})
		self.bw01.reparentTo(self.render)
		self.bw01.setScale(0.04)
		self.bw01.setPos(215, 200, 14)
		self.bw01.setHpr(30,0,0)
		self.bw01.loop('bw02')
		self.bw01.loop('bw03')
		
		self.bromanactormodel = Actor("models/bromanactormodel",{"dance":"models/bromanactoranim","dance1":"models/bromanactoryeahanim"})
		self.bromanactormodel.reparentTo(self.render)
		self.bromanactormodel.setScale(4)
		self.bromanactormodel.setPos(200, -120, 7)
		self.bromanactormodel.setHpr(90,0,0)
		self.bromanactormodel.loop('dance')
		#self.bromanactormodel.play('dance1')
		self.bromancar = self.loader.loadModel("models/bromancar")
		self.bromancar.reparentTo(self.render)
		self.bromancar.setScale(4)
		self.bromancar.setPos(199, -120, 5)
		self.bromancar.setHpr(90,0,0)
		
		self.bromanactormode2 = Actor("models/bromanactormodel",{"dance":"models/bromanactoranim","dance1":"models/bromanactoryeahanim"})
		self.bromanactormode2.reparentTo(self.render)
		self.bromanactormode2.setScale(4)
		self.bromanactormode2.setPos(210, -140, 7)
		self.bromanactormode2.setHpr(90,0,0)
		self.bromanactormode2.loop('dance')
		#self.bromanactormodel.play('dance1')
		self.bromancar = self.loader.loadModel("models/bromancar")
		self.bromancar.reparentTo(self.render)
		self.bromancar.setScale(4)
		self.bromancar.setPos(209, -140, 5)
		self.bromancar.setHpr(90,0,0)
		
		self.bromanactormode3 = Actor("models/bromanactormodel",{"dance":"models/bromanactoranim","dance1":"models/bromanactoryeahanim"})
		self.bromanactormode3.reparentTo(self.render)
		self.bromanactormode3.setScale(4)
		self.bromanactormode3.setPos(220, -160, 7)
		self.bromanactormode3.setHpr(90,0,0)
		self.bromanactormode3.loop('dance')
		#self.bromanactormodel.play('dance1')
		self.bromancar = self.loader.loadModel("models/bromancar")
		self.bromancar.reparentTo(self.render)
		self.bromancar.setScale(4)
		self.bromancar.setPos(219, -160, 5)
		self.bromancar.setHpr(90,0,0)
		
		self.bromanactormode4 = Actor("models/bromanactormodel",{"dance":"models/bromanactoranim","dance1":"models/bromanactoryeahanim"})
		self.bromanactormode4.reparentTo(self.render)
		self.bromanactormode4.setScale(4)
		self.bromanactormode4.setPos(210, -180, 7)
		self.bromanactormode4.setHpr(90,0,0)
		self.bromanactormode4.loop('dance')
		#self.bromanactormodel.play('dance1')
		self.bromancar = self.loader.loadModel("models/bromancar")
		self.bromancar.reparentTo(self.render)
		self.bromancar.setScale(4)
		self.bromancar.setPos(209, -180, 5)
		self.bromancar.setHpr(90,0,0)
		
		self.bromanactormode5 = Actor("models/bromanactormodel",{"dance":"models/bromanactoranim","dance1":"models/bromanactoryeahanim"})
		self.bromanactormode5.reparentTo(self.render)
		self.bromanactormode5.setScale(4)
		self.bromanactormode5.setPos(200, -200, 7)
		self.bromanactormode5.setHpr(90,0,0)
		self.bromanactormode5.loop('dance')
		#self.bromanactormodel.play('dance1')
		self.bromancar = self.loader.loadModel("models/bromancar")
		self.bromancar.reparentTo(self.render)
		self.bromancar.setScale(4)
		self.bromancar.setPos(199, -200, 5)
		self.bromancar.setHpr(90,0,0)
		
		
		self.goose = Actor("models/goosemodel",{"goosefly":"models/gooseanimation"})
		self.goose.reparentTo(self.render)
		self.goose.setScale(0.5)
		self.goose.setPos(0, 100, 250)		
		self.goose.setHpr(50,0,0)
		self.goose.loop('goosefly')
		seq1 = self.goose.posInterval(20, Point3(2500, 2000, 250))
		seq2 = self.goose.posInterval(0, Point3(900, -100, 250))
		seq3 = self.goose.hprInterval(0, Point3(130, 0, 0), startHpr = Point3(0, 0, 0))
		seq4 = self.goose.posInterval(20, Point3(-1500, 2000, 250))
		seq5 = self.goose.posInterval(0, Point3(0, -100, 250))
		seq6 = self.goose.hprInterval(0, Point3(0, 0, 0), startHpr = Point3(130, 0, 0))
		seq = Sequence(seq1, seq2, seq3, seq4, seq5, seq6)
		seq.loop()
		
		self.lollipop = []
		for i in xrange(15):
			lollipop = self.loader.loadModel("models/lollipop")
			lollipop.reparentTo(self.render)
			lollipop.setScale(15)
			x = random.randint(-300,300)
			y = random.randint(-300,300)
			lollipop.setPos(x, y, 0)
			self.lollipop.append(lollipop)
		
		self.mint = []
		for i in xrange(10):
			mint = self.loader.loadModel("models/Capsule")
			mint.reparentTo(self.render)
			mint.setScale(0.5)
			x = random.randint(-300,300)
			y = random.randint(-300,300)
			mint.setPos(x, y, 5)
			self.mint.append(mint)
			
		self.elixir = self.loader.loadModel("models/Bottle")
		self.elixir.reparentTo(self.render)
		self.elixir.setScale(10)
		self.elixir.setPos(self.bridge.getPos())

		self.candle = self.loader.loadModel("models/candle")
		self.candle.reparentTo(self.render)
		self.candle.setScale(0.15,0.15,0.05)
		self.candle.setPos(-340, 270 , 5)

		self.boy = Actor("models/ralph",{"walk":"models/ralph-walk","run":"models/ralph-run"})
		self.boy.reparentTo(self.render)
		self.boy.setPos(0, -300, 0)
		self.boy.setScale(2, 2, 1.5)
		self.boy.setHpr(180, 0, 0)
		self.startPos = self.boy.getPos()
		self.isMoving = False
		self.rotateBack = False
		self.rotateLeft = False
		self.rotateRight = False
		self.myAnimControl = self.boy.getAnimControl('run')

		self.monster = Actor("models/monster1",{"run":"models/monster1-tentacle-attack"})
		self.monster.reparentTo(self.render)
		self.monster.setScale(3)
		self.monster.setPos(0,-325, 5)
		self.monster.setHpr(90, 90, 90)
			
		self.jets = self.loader.loadModel("models/GreenJumpJet")
		self.jets.reparentTo(self.boy)
		self.jets.setPos(0, 500, 10)
		self.jets.setZ(0)
		self.jets.setHpr(180,0,0)
		
		#Set up the main GUI Menu shown at the startup
		maps = loader.loadModel('models/button_maps')
		self.startBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.2, text = START_BUT_TEXT, text_scale = 0.2, pos = (0, 0, 0.3), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_RESET, STATE_STARTED])
		self.exitBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.2, text = EXIT_BUT_TEXT, text_scale = 0.2, pos = (0, 0, -0.3), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_PAUSED, STATE_EXIT])
		self.optionsBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.2, text = OPTION_BUT_TEXT, text_scale = 0.2, pos = (0, 0, 0.1), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_RESET, STATE_PREFS])
		self.aboutBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.2, text = CREDITS_BUT_TEXT, text_scale = 0.2, pos = (0, 0, -0.1), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [None, None])
		
		#Set up the preferences GUI menu and then hide it
		self.labelFullScreen = DirectLabel(text = FULLSCREEN_LABEL, scale = 0.06, pos = (-0.9 , 0, 0))
		self.fullScreenBut = DirectCheckButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.15, text = FULLSCREEN_BUT_TEXT, text_scale = 0.3, pos = (0.7, 0, 0), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, indicatorValue = 0, command = self.toggleScreen)
		
		self.labelSound = DirectLabel(text = SOUND_LABEL, scale = 0.06, pos = (-0.9 , 0, 0.4))
		self.audioBut = DirectCheckButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.15, text = AUDIO_BUT_TEXT, text_scale = 0.3, pos = (0.7, 0, 0.4), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, indicatorValue = 1, command = self.toggleAudio)
		
		#self.resolutionSlider = DirectSlider(range = (0,100), value = 100, pageSize = 25, pos = (0.7, 0, 0), scale = 0.5, command = self.setResolution)
		#self.labelResolution = DirectLabel(text = RESOLUTION_LABEL, scale = 0.06, pos = (-0.9 , 0, 0))
		
		self.lightsBut = DirectCheckButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.15, text = LIGHT_BUT_TEXT, text_scale = 0.3, pos = (0.7, 0, 0.2), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.toggleLights, indicatorValue = 1)
		self.labelLights = DirectLabel(text = LIGHTS_LABEL, scale = 0.06, pos = (-0.9 , 0, 0.2))
		
		self.backBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = (0.3,0.2,0.2), text = BACK_BUT_TEXT, text_scale = 0.3, pos = (0, 0, -0.4), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_PREFS, STATE_RESET])

		
		self.gameOverLabel = DirectLabel(text = GAME_OVER_LABEL + str(self.curScore), scale = 0.1, pos = (-0.3 , 0, 0.6))
		self.submitScore = DirectEntry(text = "" , scale = (0.1, 0.07, 0.06),pos = (-1, 0, 0.3), initialText="Gamers call you?", numLines = 2,focus=1)		
		self.submitBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = (0.2,0.2,0.2), text = "SUBMIT SCORE", text_scale = 0.2, pos = (0.8, 1, 0.3), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound)
		self.playAgainBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = (0.2,0.2,0.2), text = "PLAY AGAIN", text_scale = 0.2, pos = (0, 1, 0), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_GAME_OVER, STATE_STARTED])
		self.backBut1 = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = (0.3,0.2,0.2), text = BACK_BUT_TEXT, text_scale = 0.3, pos = (0, 0, -0.4), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_GAME_OVER, STATE_RESET])	
		
		#Here helpBut is in main menu while the later one is in the help menu both at the same location giving a feel that same but is used
		self.helpBut = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = 0.2, text = HELP_BUT_TEXT, text_scale = 0.2, pos = (1, 0, -0.8), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_PAUSED, STATE_HELP])
		self.backBut2 = DirectButton(geom = (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), scale = (0.3,0.2,0.2), text = BACK_BUT_TEXT, text_scale = 0.3, pos = (1, 0, -0.8), rolloverSound = self.butHoverSound, clickSound = self.butHoverSound, command = self.switchState, extraArgs = [STATE_HELP, STATE_RESET])	
		
		self.hidePrefs()
		self.hideGameOverMenu()
		
		self.load2dObjects()
		self.hideHelpMenu()
		self.setGameElementVisiblity(False)
		
	def setGameElementVisiblity(self,args):
		if args:
			self.powerBar.show()
			self.healthBar.show()
			self.countLabel.show()
			self.lifeLabel.show()
		else:
			self.healthBar.hide()
			self.powerBar.hide()
			self.countLabel.hide()
			self.lifeLabel.hide()
		
	def switchState(self, curState, nextState):
		if curState == STATE_RESET and nextState == STATE_STARTED:
			self.hideMainMenu()
			taskMgr.remove("SpinCameraTask")
			props = WindowProperties()
			props.setCursorHidden(True)
			base.win.requestProperties(props)
			self.ambientLight.setColor(Vec4(.3, .3, .3, 1))
			self.transit.letterboxOff(2.5)
			self.setGameElementVisiblity(True)
		elif curState == STATE_RESET and nextState == STATE_PREFS: 
			self.hideMainMenu()
			self.showPrefs()
			
		#All these will be when current state is Prefs
		elif curState == STATE_PREFS and nextState == STATE_RESET:
			self.hidePrefs()
			self.showMainMenu()
		
		#All these will be when current state is started
		elif curState == STATE_STARTED and nextState == STATE_PAUSED:
			self.transit.letterboxOn(2.5)
			self.showMainMenu()
			self.optionsBut.hide()
			self.aboutBut.hide()
			self.optionsBut.hide()
			self.helpBut.hide()
			self.startBut['text'] = "RESUME GAME"
			props = WindowProperties()
			props.setCursorHidden(False) 
			base.win.requestProperties(props)
			taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		elif curState == STATE_STARTED and nextState == STATE_GAME_OVER:
			self.showGameOverMenu()
			self.gameOverLabel["text"] = GAME_OVER_LABEL + str(self.curScore)
			self.transit.letterboxOn(2.5)
			props = WindowProperties()
			props.setCursorHidden(False) 
			base.win.requestProperties(props)
			self.setGameElementVisiblity(False)
			
		#All these will be when current state are Paused
		elif curState == STATE_PAUSED and nextState == STATE_STARTED:
			self.transit.letterboxOff(2.5)
			self.hideMainMenu()
			self.startBut['text'] = "PLAY"
			props = WindowProperties()
			props.setCursorHidden(True) 
			base.win.requestProperties(props)
			taskMgr.remove("SpinCameraTask")
		elif curState == STATE_PAUSED and nextState == STATE_EXIT:
			#maps = loader.loadModel('models/button_maps')
			#geomList = [(maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable')), (maps.find('**/but_steady'),maps.find('**/but_click'),maps.find('**/but_hover'),  maps.find('**/but_disable'))]
			self.askDialog = YesNoDialog(dialogName="YesNoCancelDialog", text = EXIT_TEXT, buttonTextList = ["YES", "NO"], buttonSize = [-0.5,0.5,-0.05,0.1], fadeScreen = 1, command = self.quit)
		elif curState == STATE_PAUSED and nextState == STATE_HELP: 
			self.hideMainMenu()
			self.showHelpMenu()
			
		#All thes have game over as start state
		elif curState == STATE_GAME_OVER and nextState == STATE_STARTED:
			self.boy.setPos(5, -210, 0)
			self.monster.setPos(0,-325, 5)
			self.keyMap = {"left":0, "right":0, "forward":0, "back":0}
			self.hasJet = False
			self.nearCarousel = False
			self.nearOctopus = False
			self.nearSkyride = False
			self.nearTent = False
			self.nearHouse = False
			self.nearCoaster = False
			self.nearLollipop = False
			self.nearMint = False
			self.nearMonster = False
			self.pose = False
			self.nearBridge = False
			self.hasBoost = False
			self.boostCount = 100
			self.curScore = 0
			self.noOfLives = 2
			self.hasGhostPower = False
			self.countMonster = 300
			self.boyHealth = 100
			self.healthBar['value'] = 100
			self.countLabel['text'] = str(0)
			self.lifeLabel['text'] = str(2)
			self.hideGameOverMenu()
			self.transit.letterboxOff(2.5)
			self.setGameElementVisiblity(True)
		elif curState == STATE_GAME_OVER and nextState == STATE_RESET:
			self.boy.setPos(5, -210, 0)
			self.monster.setPos(0,-325, 5)
			self.keyMap = {"left":0, "right":0, "forward":0, "back":0}
			self.hasJet = False
			self.nearCarousel = False
			self.nearOctopus = False
			self.nearSkyride = False
			self.nearTent = False
			self.nearHouse = False
			self.nearCoaster = False
			self.nearLollipop = False
			self.nearMint = False
			self.nearMonster = False
			self.pose = False
			self.nearBridge = False
			self.hasBoost = False
			self.boostCount = 100
			self.curScore = 0
			self.noOfLives = 2
			self.hasGhostPower = False
			self.showMainMenu()
			self.hideGameOverMenu()
			self.healthBar['value'] = 100
			self.countLabel['text'] = str(0)
			self.lifeLabel['text'] = str(2)
			self.countMonster = 300
			self.boyHealth = 100
			self.setGameElementVisiblity(True)
			self.startBut['text'] = START_BUT_TEXT
		
		#This contains all the states with help as curent state
		elif curState == STATE_HELP and nextState == STATE_RESET:
			self.hideHelpMenu()
			self.showMainMenu()
		
		if curState != None and nextState != None:
			self.curState = nextState	
		else:
			self.aboutUsDialog = YesNoCancelDialog(dialogName="okDialog", text = ABOUT_US_TEXT, buttonTextList = ["YES", "NO", "GO BACK"], buttonSize = [-0.5,0.5,-0.05,0.1], fadeScreen = 1, command = self.aboutUs)
		
app = MyApp()
app.run()
