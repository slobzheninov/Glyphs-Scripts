#MenuTitle: Demo Instances Generator
# -*- coding: utf-8 -*-
__doc__ = """
Generates demo instances with limited character set and features from active instances. Accepts glyph names separated by spaces.
"""
import copy
import vanilla
from Foundation import NSUserDefaults
from GlyphsApp import Glyphs, GSCustomParameter

Glyphs.clearLog()

thisFont = Glyphs.font

m = 15  # margin
tm = 35  # top/vertical margin
bm = 50  # bottom margin


class DemoFontsGenerator(object):

	def __init__(self):
		# Window 'self.w':
		windowWidth = 200
		windowHeight = 360
		windowWidthResize = 1200  # user can resize width by this value
		windowHeightResize = 500  # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),  # default window size
			"Demo Instances Generator",  # window title
			minSize=(windowWidth, windowHeight),  # minimum size (for resizing)
			maxSize=(windowWidth + windowWidthResize, windowHeight + windowHeightResize),  # maximum size (for resizing)
			autosaveName="save.DemoInstancesGenerator.mainwindow"  # stores last window position and size
		)


		# UI elements:

		self.w.text_name = vanilla.TextBox((m, m - 3, windowWidth, tm), "Name (Suffix):", sizeStyle='small')
		self.w.text_glyphs = vanilla.TextBox((m, tm * 2 + m - 3, windowWidth, tm), "Limited Character Set:", sizeStyle='small')

		self.w.name = vanilla.TextEditor((m, tm, windowWidth - m * 2, tm), callback=self.SavePreferences, checksSpelling=False)
		self.w.glyphs = vanilla.TextEditor((m, tm * 3, windowWidth - m * 2, -bm), callback=self.SavePreferences, checksSpelling=False)

		self.windowResize(None)

		# Run Button:
		self.w.runButton = vanilla.Button((-80 - m, -20 - m, -m, m), "Generate", sizeStyle='regular', callback=self.generateDemoInstances)
		self.w.setDefaultButton(self.w.runButton)

		# Reset Button:
		self.w.resetButton = vanilla.Button(((-80 - m) * 2, -20 - m, (-80 - m) - m, m), "Reset", sizeStyle='regular', callback=self.ResetParameters)

		self.w.bind("resize", self.windowResize)

		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Demo Fonts Generator' could not load preferences. Will resort to defaults")

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def windowResize(self, sender):
		windowWidth = self.w.getPosSize()[2]
		adaptiveWidth = windowWidth - m * 2

		self.w.name.setPosSize((m, tm, adaptiveWidth, tm))
		self.w.glyphs.setPosSize((m, tm * 3, adaptiveWidth, -bm))

	def SavePreferences(self, sender):
		try:
			Glyphs.defaults["save.DemoInstancesGenerator.name"] = self.w.name.get()
			Glyphs.defaults["save.DemoInstancesGenerator.glyphs"] = self.w.glyphs.get()
		except:
			return False
		return True

	def LoadPreferences(self):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_({
				"save.DemoInstancesGenerator.name": "Demo",
				"save.DemoInstancesGenerator.glyphs": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z zero one two three four five seven eight period comma space hyphen b.calt f.calt h.calt k.calt l.calt f_t t_t A-cy Be-cy Ve-cy Ge-cy De-cy Ie-cy Io-cy Zhe-cy Ze-cy Ii-cy Iishort-cy Ka-cy El-cy Em-cy En-cy O-cy Pe-cy Er-cy Es-cy Te-cy U-cy Ef-cy Ha-cy Tse-cy Che-cy Sha-cy Shcha-cy Yeru-cy Softsign-cy Ereversed-cy Iu-cy Ia-cy a-cy be-cy ve-cy ge-cy de-cy ie-cy io-cy zhe-cy ze-cy ii-cy iishort-cy ka-cy el-cy em-cy en-cy o-cy pe-cy er-cy es-cy te-cy u-cy ef-cy ha-cy tse-cy che-cy sha-cy shcha-cy yeru-cy softsign-cy ereversed-cy iu-cy ia-cy .notdef ",
			})
			self.w.name.set(Glyphs.defaults["save.DemoInstancesGenerator.name"])
			self.w.glyphs.set(Glyphs.defaults["save.DemoInstancesGenerator.glyphs"])
		except:
			return False

		return True

	def ResetParameters(self, sender):
		del Glyphs.defaults["save.DemoInstancesGenerator.name"]
		del Glyphs.defaults["save.DemoInstancesGenerator.glyphs"]
		self.w.name.set(Glyphs.defaults["save.DemoInstancesGenerator.name"])
		self.w.glyphs.set(Glyphs.defaults["save.DemoInstancesGenerator.glyphs"])

	def generateDemoInstances(self, sender):

		# pass glyph or class names here
		def replaceFeatureParameter(name):
			for fname, fcode in newFeatures.items():
				if (" %s ") % (name) in fcode or (" %s;") % (name) in fcode or (" %s' ") % (name) in fcode:
					newFeatureCode = ''
					for line in fcode.splitlines():
						if line.find(name) < 0:
							newFeatureCode = newFeatureCode + line + "\n"

					if len(newFeatureCode) == 0:
						if fname not in featuresToRemove:
							featuresToRemove.append(fname)
							newFeatures.pop(fname)
					else:
						newFeatures[fname] = newFeatureCode

		# glyphs and name to keep
		demoName = self.w.name.get()
		demoGlyphs = " %s " % (self.w.glyphs.get())
		demoGlyphsList = list(demoGlyphs.split(" "))

		# list glyphs to remove
		featuresToRemove = []
		classesToRemove = []
		replaceClasses = {}
		# replaceFeatures = {}

		newFeatures = {}
		for feature in thisFont.features:
			if feature.active == 1 and not feature.automatic:
				newFeatures[feature.name] = feature.code

		for glyph in thisFont.glyphs:
			if (" %s ") % (glyph.name) not in demoGlyphs:
				print('not in demo glyphs', glyph.name)
				# Replace Class custom parameter
				for GSClass in thisFont.classes:
					if GSClass.active == 1:
						if (" %s ") % glyph.name in (' %s ') % GSClass.code:
							print('----', glyph.name, GSClass.name)
							if GSClass.name not in replaceClasses.keys():
								temp = (' %s ' % GSClass.code).replace(' %s ' % glyph.name, ' ')
								# if code is not empty, otherwise remove the class
								if temp.strip() != '':
									replaceClasses[GSClass.name] = temp.rstrip().lstrip()
								else:
									classesToRemove += GSClass.name
									replaceClasses.pop(GSClass.name)
							else:
								temp = (' %s ' % replaceClasses[GSClass.name]).replace(' %s ' % glyph.name, ' ')
								# if code is not empty, otherwise remove the class
								if temp.strip() != '':
									replaceClasses[GSClass.name] = temp.rstrip().lstrip()
								else:
									classesToRemove.append(GSClass.name)
									replaceClasses.pop(GSClass.name)

				# Replace Feature custom parameter (glyphs)
				replaceFeatureParameter(glyph.name)

		# Replace Feature custom parameter (empty classes)
		for GSClass in classesToRemove:
			replaceFeatureParameter('@%s' % GSClass)

		# remove features with no sub or pos
		for fname, fcode in newFeatures.items():
			if 'sub' not in fcode and 'pos' not in fcode:
				featuresToRemove.append(fname)
				newFeatures.pop(fname)

		print('delete features: %s\n' % featuresToRemove)
		print('newFeatures: %s\n' % newFeatures)
		print('replaced Classes: %s\n' % replaceClasses)
		print('Remove Classes: %s\n' % classesToRemove)

		# Create copies of active instances, add limiting custom parameters, add Demo naming
		def copyInstances():
			demoInstances = ""  #list of demo instances

			for instance in thisFont.instances:
				if instance.active and (demoName in instance.name):
					demoInstances += "%s, " % instance.name

			for instance in thisFont.instances:
				if instance.active:
					# check if demo already exists
					if (("%s %s") % (instance.name, demoName) in demoInstances) or (demoName in instance.name):
						if demoName in instance.name:
							print("%s already exists" % instance.name)

					# if demo doesn't exist
					else:
						# copy active instances
						newInstance = copy.copy(instance)
						thisFont.instances.append(newInstance)

						# Demo preferredFamily (check if exists or use familyName)
						if newInstance.customParameters["preferredFamilyName"]:
							demoFamilyName = ("%s %s") % (newInstance.customParameters["preferredFamilyName"], demoName)
							newInstance.customParameters["preferredFamilyName"] = demoFamilyName
							#print(newInstance.customParameters)
						else:
							demoFamilyName = ("%s %s") % (thisFont.familyName, demoName)
							newInstance.customParameters["preferredFamilyName"] = demoFamilyName

						# Demo preferredSubfamily (check if exists or use instance name)
						if not newInstance.customParameters["preferredSubfamilyName"]:
							newInstance.customParameters["preferredSubfamilyName"] = newInstance.name


						# rename Demo instance (in Glyphs only)
						newInstance.name = ("%s %s") % (newInstance.name, demoName)
						#add it to the list
						demoInstances += "+ %s, " % newInstance.name


						# rename font files
						newInstance.customParameters["fileName"] = "%s - %s" % (newInstance.customParameters["preferredFamilyName"], newInstance.customParameters["preferredSubfamilyName"])


						# limit glyphs
						newInstance.customParameters["Keep Glyphs"] = demoGlyphsList

						# limit classes
						for cname, ccode in replaceClasses.items():
							newInstance.customParameters.append(GSCustomParameter("Replace Class", '%s; %s' % (cname, ccode)))
						if classesToRemove:
							newInstance.customParameters.append(GSCustomParameter("Remove Classes", classesToRemove))

						# limit features
						for fname, fcode in newFeatures.items():
							newInstance.customParameters.append(GSCustomParameter("Replace Feature", '%s; %s' % (fname, fcode)))
						if featuresToRemove:
							newInstance.customParameters.append(GSCustomParameter("Remove Features", featuresToRemove))

						# update features parameter?
						#newInstance.customParameters["Update Features"] = True

		copyInstances()


DemoFontsGenerator()
