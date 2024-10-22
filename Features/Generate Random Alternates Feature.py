#MenuTitle: Generate Random Alternates Feature
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a Random Alternates feature (calt by default). Replaces the existing feature code, if any.
Run the script and read the comment in the OT feature for an explanation. For more info, github.com/slobzheninov
"""

import objc
from random import choice, randint
from vanilla import FloatingWindow, TextBox, EditText, TextEditor, Button
from GlyphsApp import Glyphs, GSClass, GSFeature

font = Glyphs.font
Glyphs.clearLog()


comment = """# This is your random feature!
# Here’s how it works:
# 1. Glyphs from the selected Categories are randomly added to the selected number of Classes (called rand...).
# 2. Then glyphs and its alternatives are randomly placed in 'sub... by ...' sequences of the chosen length.
# 3. That can be repeated a few times, depending on how many lookups and lines per lookup you choose.
# Input format: glyph and its alternatives space separated. Next glyph with its alternatives go to the next line
"""

GSSteppingTextField = objc.lookUpClass("GSSteppingTextField")


class ArrowEditText (EditText):
	nsTextFieldClass = GSSteppingTextField

	def _setCallback(self, callback):
		super(ArrowEditText, self)._setCallback(callback)
		if callback is not None:  # and self._continuous:
			self._nsObject.setContinuous_(True)
			self._nsObject.setAction_(self._target.action_)
			self._nsObject.setTarget_(self._target)


class RandomFeature:

	def __init__(self):
		W, H = 400, 250
		Wmax, Hmax = 1000, 1000

		M = 10
		buttonWidth = 80
		inputWidth = buttonWidth * .6

		self.w = FloatingWindow((W, H), 'Random Feature', minSize=(W, H), maxSize=(Wmax, Hmax))

		self.w.glyphs = TextEditor((M, M, -M, -M * 14), 'a a.ss01 a.ss02\nb b.ss01 b.ss02')

		# column 1
		self.w.featureTitle = TextBox((M, -M * 13, buttonWidth, M * 3), 'Feature')
		self.w.feature = EditText((M * 2 + buttonWidth, -M * 13.1, inputWidth, M * 2.5), 'calt')

		self.w.linesTitle = TextBox((M, -M * 10, buttonWidth, M * 3), 'Lines')
		self.w.lines = ArrowEditText((M * 2 + buttonWidth, -M * 10.1, inputWidth, M * 2.5), '20', continuous=False, callback=self.editTextCallback)

		self.w.sequenceTitle = TextBox((M, -M * 7, buttonWidth, M * 3), 'Sequence')
		self.w.sequence = ArrowEditText((M * 2 + buttonWidth, -M * 7.1, inputWidth, M * 2.5), '3', continuous=False, callback=self.editTextCallback)

		# column 2
		self.w.categoriesTitle = TextBox((M * 3 + buttonWidth * 1.7, -M * 13, buttonWidth, M * 3), 'Categories')
		self.w.categories = EditText((M * 3 + buttonWidth * 2.7, -M * 13.1, -M, M * 2.5), 'Letter Punctuation')

		self.w.lookupsTitle = TextBox((M * 3 + buttonWidth * 1.7, -M * 10, buttonWidth, M * 3), 'Lookups')
		self.w.lookups = ArrowEditText((M * 3 + buttonWidth * 2.7, -M * 10.1, inputWidth, M * 2.5), '4', continuous=False, callback=self.editTextCallback)

		self.w.classesTitle = TextBox((M * 3 + buttonWidth * 1.7, -M * 7, buttonWidth, M * 3), 'Classes')
		self.w.classes = ArrowEditText((M * 3 + buttonWidth * 2.7, -M * 7.1, inputWidth, M * 2.5), '5', continuous=False, callback=self.editTextCallback)

		self.w.runButton = Button((-M - buttonWidth, -M * 4, buttonWidth, M * 3), 'Run', callback=self.runCallback)

		self.w.open()

	def editTextCallback(self, sender):
		# int input only!
		inpt = sender.get()
		try:
			sender.set(str(int(inpt)))
		except:
			sender.set('3')

	def runCallback(self, sender):
		glyphs = {}

		# ---------- user input
		# get glyphs dict from user’s input, ignore missing glyphs
		inpt = self.w.glyphs.get()
		for line in inpt.split('\n'):
			alts = line.split()
			if alts:
				default = alts[0]
				if default:
					existingAlts = []
					missingAlts = []
					for i in range(len(alts) - 1):
						# check if requested alternatives are in the font
						for alt in alts:
							if alt in font.glyphs:
								if alt not in existingAlts:
									existingAlts.append(alt)
							else:
								missingAlts.append(alt)
						# add to the dict
						if existingAlts:
							glyphs[default] = existingAlts

						if missingAlts:
							# report missing alternatives
							print('Glyphs not found are ignored:')
							print(missingAlts)

		# other input
		try:
			featureName = self.w.feature.get()
			categories = self.w.categories.get().split()
			classesToAdd = int(self.w.classes.get())
			linesToAdd = int(self.w.lines.get())
			lookupsToAdd = int(self.w.lookups.get())
			sequence = int(self.w.sequence.get())
		except:
			print('Couldn’t read the input')
			return


		# ---------- classes
		# make classes
		classes = []

		for i in range(classesToAdd):
			className = 'rand%s' % i
			classes.append(GSClass(className, ''))


		# add glyphs to the classes
		for glyph in font.glyphs:
			if glyph.category in categories and glyph.export:
				classIndex = randint(0, classesToAdd - 1)
				classes[classIndex].code += '%s ' % glyph.name

		# add classes to the font
		for clas in classes:
			classExists = False
			for clas2 in font.classes:
				if clas2.name == clas.name:
					clas2.code = clas.code
					classExists = True
					break
			if classExists is False:
				font.classes.append(clas)


		# ---------- feature
		# build code
		code = comment + '\n'

		for lookupIndex in range(lookupsToAdd):
			code += 'lookup random%s {\n' % lookupIndex

			for l in range(linesToAdd):
				line = '\tsub '
				glyphFrom = choice(list(glyphs))

				# avoid sub A by A
				for i in range(10):
					glyphTo = choice(glyphs[glyphFrom])
					if glyphFrom != glyphTo:
						break

				targetGlyphIndex = randint(0, sequence - 1)
				for i in range(sequence):
					if i == targetGlyphIndex:
						line += '%s\' ' % glyphFrom
					else:
						line += '@rand%s ' % randint(0, classesToAdd - 1)
				line += 'by %s;' % glyphTo
				code += line + '\n'

			code += '} random%s;\n\n' % lookupIndex


		# add feature to the font
		featureExists = False
		for feature in font.features:
			if feature.name == featureName:
				feature.code = code
				featureExists = True
				break
		if featureExists is False:
			newFeature = GSFeature(featureName, code)
			font.features.append(newFeature)

		# compile features
		font.compileFeatures()


RandomFeature()
