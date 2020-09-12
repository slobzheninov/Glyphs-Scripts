#MenuTitle: Demo Instances Generator
# -*- coding: utf-8 -*-
__doc__="""
Generates demo instances with limited character set and features from active instances
"""
import copy
import string
import vanilla
from Foundation import NSUserDefaults, NSString



m = 15 # margin
tm = 35 # top/vertical margin
bm = 50 # bottom margin
h = 100 # text editor height

class DemoFontsGenerator ( object ):
	
	def __init__(self):
		# Window 'self.w':
		windowWidth  = 200
		windowHeight = 360
		windowWidthResize  = 1200 # user can resize width by this value
		windowHeightResize = 500 # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Demo Instances Generator", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "save.DemoInstancesGenerator.mainwindow" # stores last window position and size
		)
		
		
		# UI elements:
			
		self.w.text_name = vanilla.TextBox( (m, m-3, windowWidth, tm), "Name (Suffix):", sizeStyle='small' )
		self.w.text_features = vanilla.TextBox( (m, h*2+tm*2+m-3, windowWidth, tm), "Limited Character Set:", sizeStyle='small' )
		self.w.text_chars = vanilla.TextBox( (m, h+tm+m-3, windowWidth, tm), "Limited Features:", sizeStyle='small' )

		self.w.name = vanilla.TextEditor( (m, tm, windowWidth-m*2, tm), callback=self.SavePreferences, checksSpelling=False )
		self.w.chars = vanilla.TextEditor( (m, tm*3, windowWidth-m*2, h), callback=self.SavePreferences, checksSpelling=False )
		self.w.features = vanilla.TextEditor( (m, tm*4+h, windowWidth-m*2, h), callback=self.SavePreferences, checksSpelling=False )
		
		
		self.windowResize(None)
		
		# Run Button:
		self.w.runButton = vanilla.Button((-80-m, -20-m, -m, m), "Generate", sizeStyle='regular', callback=self.DemoFontsGeneratorParameters )
		self.w.setDefaultButton( self.w.runButton )
		
		# Reset Button:
		self.w.resetButton = vanilla.Button(((-80-m)*2, -20-m, (-80-m)-m, m), "Reset", sizeStyle='regular', callback=self.ResetParameters )
		#self.w.setDefaultButton( self.w.resetButton )
		
		self.w.bind("resize",self.windowResize)
		
		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Demo Fonts Generator' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
	
	
	def windowResize( self, sender ):
		windowWidth = self.w.getPosSize()[2]
		windowHeight = self.w.getPosSize()[3]
		adaptiveWidth = windowWidth - m*2
		adaptiveHeight = windowHeight / 2 - (tm * 4 + bm) / 2
		
		self.w.text_features.setPosSize( (m, tm*2+m-3, adaptiveWidth, adaptiveHeight) )
		self.w.text_chars.setPosSize( (m, adaptiveHeight+tm*3+m-3, adaptiveWidth, tm) )
		
		self.w.name.setPosSize( (m, tm, adaptiveWidth, tm) )
		self.w.chars.setPosSize( (m, tm*3, adaptiveWidth, adaptiveHeight) )
		self.w.features.setPosSize( (m, tm*4+adaptiveHeight, adaptiveWidth, adaptiveHeight ) )
		
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["save.DemoInstancesGenerator.name"] = self.w.name.get()
			Glyphs.defaults["save.DemoInstancesGenerator.chars"] = self.w.chars.get()
			Glyphs.defaults["save.DemoInstancesGenerator.features"] = self.w.features.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"save.DemoInstancesGenerator.name": "Demo",
					"save.DemoInstancesGenerator.chars": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 . , - space",
					"save.DemoInstancesGenerator.features": "ss01"
				}
			)
			self.w.name.set( Glyphs.defaults["save.DemoInstancesGenerator.name"] )
			self.w.chars.set( Glyphs.defaults["save.DemoInstancesGenerator.chars"] )
			self.w.features.set( Glyphs.defaults["save.DemoInstancesGenerator.features"] )
		except:
			return False
			
		return True
		
		
	def ResetParameters ( self, sender):
		del Glyphs.defaults["save.DemoInstancesGenerator.name"]
		del Glyphs.defaults["save.DemoInstancesGenerator.chars"]
		del Glyphs.defaults["save.DemoInstancesGenerator.features"]
		self.w.name.set( Glyphs.defaults["save.DemoInstancesGenerator.name"] )
		self.w.chars.set( Glyphs.defaults["save.DemoInstancesGenerator.chars"] )
		self.w.features.set( Glyphs.defaults["save.DemoInstancesGenerator.features"] )

		
		
	def DemoFontsGeneratorParameters (self, sender):
		demoName = self.w.name.get()
		demoGlyphs = self.w.chars.get()
		demoFeatures = self.w.features.get()
		

		# ----------- Customize -----------
		"""
		demoName = "Demo" # Demo or Trial or Test or whatever
		demoGlyphs = ("%s%s .,- Aacute") %(string.ascii_letters, string.digits) # limited glyph set
		demoFeatures = "" # limited features, if any
		"""
		# ---------------------------------


		thisFont = Glyphs.fonts[0] # frontmost font
		thisInstance = thisFont.instances


		# list glyphs to remove
		removeGlyphs = ""
		for glyph in thisFont.glyphs:
			if glyph.string not in demoGlyphs:
				if glyph.name not in demoGlyphs:
					removeGlyphs += ("%s, ") %(glyph.name)		
					
			
		# list features to remove
		removeFeatures = ""
		for feature in thisFont.features:
			if feature.name not in demoFeatures:
				removeFeatures += ("%s, ") %(feature.name)


		# creates copies of active instances, adds limiting custom parameters, adds Demo naming
		def copyInstances():
			demoInstances = "" #list of demo instances
			
			for instance in thisFont.instances:
				if instance.active and (demoName in instance.name):
					demoInstances += "%s, " %instance.name
			
			for instance in thisFont.instances:
				if instance.active:
					
					# check if demo already exists
					if (("%s %s") %(instance.name, demoName) not in demoInstances) and (demoName not in instance.name):
						
						# copy active instances
						newInstance = copy.copy(instance)
						thisFont.instances.append(newInstance)



						# Demo preferredFamily (check if exists or use familyName)
						if newInstance.customParameters["preferredFamilyName"]:
							demoFamilyName = ("%s %s") %(newInstance.customParameters["preferredFamilyName"], demoName)
							newInstance.customParameters["preferredFamilyName"] = demoFamilyName
							#print(newInstance.customParameters)
						else:
							demoFamilyName = ("%s %s") %(thisFont.familyName, demoName)
							newInstance.customParameters["preferredFamilyName"] = demoFamilyName
						
							
							
						# Demo preferredSubfamily (check if exists or use instance name)
						if not newInstance.customParameters["preferredSubfamilyName"]:
							newInstance.customParameters["preferredSubfamilyName"] = newInstance.name



						# rename Demo instance (in Glyphs only)
						newInstance.name = ("%s %s") %(newInstance.name, demoName)
						#add it to the list
						demoInstances += "%s, " %newInstance.name
						
						
						# rename font files
						newInstance.customParameters["fileName"] = "%s - %s" %(newInstance.customParameters["preferredFamilyName"], newInstance.customParameters["preferredSubfamilyName"])
					
						
						#limit glyphs and features
						newInstance.customParameters["Remove Glyphs"] = removeGlyphs
						newInstance.customParameters["Remove Features"] = removeFeatures
						
						
					# if demo already exists				
					else:
						if demoName in instance.name:
							print("%s - already exists" %instance.name)
		copyInstances()

DemoFontsGenerator()


