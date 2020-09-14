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
		self.w.text_glyphs = vanilla.TextBox( (m, tm*2+m-3, windowWidth, tm), "Limited Character Set:", sizeStyle='small' )
		
		self.w.name = vanilla.TextEditor( (m, tm, windowWidth-m*2, tm), callback=self.SavePreferences, checksSpelling=False )
		self.w.glyphs = vanilla.TextEditor( (m, tm*3, windowWidth-m*2, -bm), callback=self.SavePreferences, checksSpelling=False )
		
		self.windowResize(None)
		
		# Run Button:
		self.w.runButton = vanilla.Button((-80-m, -20-m, -m, m), "Generate", sizeStyle='regular', callback=self.DemoFontsGeneratorParameters )
		self.w.setDefaultButton( self.w.runButton )
		
		# Reset Button:
		self.w.resetButton = vanilla.Button(((-80-m)*2, -20-m, (-80-m)-m, m), "Reset", sizeStyle='regular', callback=self.ResetParameters )
		
		self.w.bind("resize",self.windowResize)
		
		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Demo Fonts Generator' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
	
	
	def windowResize( self, sender ):
		windowWidth = self.w.getPosSize()[2]
		adaptiveWidth = windowWidth - m*2
				
		self.w.name.setPosSize( (m, tm, adaptiveWidth, tm) )
		self.w.glyphs.setPosSize( (m, tm*3, adaptiveWidth, -bm) )
		
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["save.DemoInstancesGenerator.name"] = self.w.name.get()
			Glyphs.defaults["save.DemoInstancesGenerator.glyphs"] = self.w.glyphs.get()
		except:
			return False
			
		return True


	def LoadPreferences( self ):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"save.DemoInstancesGenerator.name": "Demo",
					"save.DemoInstancesGenerator.glyphs": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 . , - space",
				}
			)
			self.w.name.set( Glyphs.defaults["save.DemoInstancesGenerator.name"] )
			self.w.glyphs.set( Glyphs.defaults["save.DemoInstancesGenerator.glyphs"] )
		except:
			return False
			
		return True
		
		
	def ResetParameters ( self, sender):
		del Glyphs.defaults["save.DemoInstancesGenerator.name"]
		del Glyphs.defaults["save.DemoInstancesGenerator.glyphs"]
		self.w.name.set( Glyphs.defaults["save.DemoInstancesGenerator.name"] )
		self.w.glyphs.set( Glyphs.defaults["save.DemoInstancesGenerator.glyphs"] )

		
		
	def DemoFontsGeneratorParameters (self, sender):

		thisFont = Glyphs.fonts[0] # frontmost font


		# glyphs and name to keep
		demoName = self.w.name.get()
		demoGlyphs = " %s " %(self.w.glyphs.get())


		# list glyphs to remove
		removeGlyphs = ""
		removeClasses = ""
		removeFeatures = ""
		
		for glyph in thisFont.glyphs:
			if (" %s ") %(glyph.string) not in demoGlyphs:
				if (" %s ") %(glyph.name) not in demoGlyphs:
					removeGlyphs += ("%s, ") %(glyph.name)	
					
					# list classes to remove
					for GSClass in thisFont.classes:						
						if ("%s ") %(glyph.name) in GSClass.code:
							if ("%s, ") %(GSClass.name) not in removeClasses:
								removeClasses += "%s, " %GSClass.name
								
								# if removed class is in a feature, list the feature to remove
								for feature in thisFont.features:
									if ("%s, ") %(feature.name) not in removeFeatures:
										if (("%s ") %(GSClass.name) in feature.code) or (("%s' ") %(GSClass.name) in feature.code) or (((" %s;") %(GSClass.name) in feature.code)):
											removeFeatures += ("%s, ") %(feature.name)	
					
					# list features to remove
					for feature in thisFont.features:
						if ("%s, ") %(feature.name) not in removeFeatures:
							if (("%s ") %(glyph.name) in feature.code) or (("%s' ") %(glyph.name) in feature.code) or (((" %s;") %(glyph.name) in feature.code)):
								removeFeatures += ("%s, ") %(feature.name)	
												
				
		print("Removed classes: %s\n" %(removeClasses))
		print(("Removed features: %s\n" %(removeFeatures)))
						

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
					
						
						#limit glyphs, features and classes
						newInstance.customParameters["Remove Glyphs"] = removeGlyphs
						newInstance.customParameters["Remove Features"] = removeFeatures
						newInstance.customParameters["Remove Classes"] = removeClasses
						
					# if demo already exists				
					else:
						if demoName in instance.name:
							print("%s already exists" %instance.name)
		copyInstances()

DemoFontsGenerator()


