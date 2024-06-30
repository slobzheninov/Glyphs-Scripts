#MenuTitle: Export To All Formats
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Export to all formats at once.
WEB formats are WOFF and WOFF2. If “PS outlines” is off, TT outlines will be exported for the web formats.
Optionally, separates formats into subfolders.
Instances with different familyNames go to different subfolders as well.
"""

from vanilla import FloatingWindow, TextBox, PopUpButton, CheckBox, SquareButton, Button, ProgressBar
import os

Glyphs.clearLog()
Glyphs3 = Glyphs.versionNumber >= 3

# window size and margin
M = 15
W, H = 380, M*19
captionWidth = 130
columnWidth = 45
lineYs = [M, M*3, M*5, M*7, M*9, M*11, M*13, M*15, M*17] # y of each line (tittle, export, outline flavor, remove overlaps, autohint)
lineYs = [y-7 for y in lineYs] # shift all vertically a bit

captions = ['', 'Export', 'Autohint', 'Remove Overlaps', 'PS Outlines']
formats = ['OTF', 'TTF', 'WEB', 'Variable', 'Variable WEB']

# No Variable WEB in Glyphs 2
if Glyphs3 is False:
	formats.remove('Variable WEB')
	W -= columnWidth

alphaActive = 1
alphaDeactivated = .4

class CheckBoxWithAlpha(CheckBox):
	def setAlpha(self, value = 1):
		self.getNSButton().setAlphaValue_(value)


class ExportToAllFormats():
	def __init__(self):
		self.exportPath = Glyphs.defaults['OTFExportPath']
		
		# window
		self.w = FloatingWindow((W, H), 'Export to all formats')

		# make captions for each row
		for i in range(len(lineYs))[:5]:
			captionID = captions[i]
			caption = TextBox((M, lineYs[i], captionWidth, M), captions[i])
			setattr(self.w, captionID, caption)

		# make a column of options for each format
		for i in range(len(formats)):
			x = captionWidth + columnWidth * i
			if i > 2: 
				x += 10 # add a gap to separate variable formats

			# format title
			formatTitle = formats[i] if i != 4 else 'WEB' # shorten 'Variable WEB' to another 'WEB'
			y = lineYs[0]
			titleID = 'title' + formats[i]
			title = TextBox((x-columnWidth/2, y, columnWidth*2, M), formatTitle, alignment = 'center')
			setattr(self.w, titleID, title)

			x += columnWidth/2 - 7
			# export checkbox
			y = lineYs[1]
			exportCheckBoxID = 'exportCheckBox' + formats[i]
			exportCheckBox = CheckBox((x, y, columnWidth/2, M), None, value = True, callback = self.exportCheckBoxCallback)
			setattr(self.w, exportCheckBoxID, exportCheckBox)
			setattr(getattr(self.w, exportCheckBoxID), 'i', i)

			# autohint checkbox
			y = lineYs[2]
			autohintID = 'autohint' + formats[i]
			autohint = CheckBoxWithAlpha((x, y, columnWidth/2, M),'', value = True)
			setattr(self.w, autohintID, autohint)
			
			# overlaps checkbox (except variable)
			if i < 3:
				y = lineYs[3]
				overlapsID = 'overlaps' + formats[i]
				overlaps = CheckBoxWithAlpha((x, y, columnWidth/2, M),'', value = True)
				setattr(self.w, overlapsID, overlaps)

			# PS outlines (web only)
			if i == 2:
				y = lineYs[4]
				outlinesID = 'outlines' + formats[i]
				outlines = CheckBoxWithAlpha((x, y, columnWidth/2, M),'')
				setattr(self.w, outlinesID, outlines)

		# Export Path
		self.w.exportPath = SquareButton((M+3, lineYs[5], -M-3, M), 'Export Path', callback = self.exportPathCallback)
		if self.exportPath:
			self.w.exportPath.setTitle(self.exportPath)

		# Export all open fonts
		self.w.exportAll = CheckBox((M, lineYs[6], W/2, M), 'All open fonts')

		# Subfolders
		self.w.subfolders = CheckBox((W/2, lineYs[6], W/2, M), 'Format subfolders', value = True)
		
		# Run button
		self.w.run = Button((W/2, lineYs[7], -M, M), 'Export', callback = self.run)
		if self.exportPath:
			self.w.exportPath.setTitle(self.exportPath)

		# progress bar
		self.w.progress = ProgressBar((M, H+100, -M, M))

		# exporting instance
		self.w.info = TextBox((M, lineYs[8], -M, M), '')

		# Uncheck variable checkboxes by default
		for ID in ['exportCheckBoxVariable', 'exportCheckBoxVariable WEB']:
			checkbox = getattr(self.w, ID, None)
			if checkbox:
				checkbox.toggle()
				self.exportCheckBoxCallback(checkbox)

		self.w.open()


	def exportCheckBoxCallback(self, sender):
		# deactivate run button if no formats are chosen for export
		countFormats = 0
		for formt in formats:
			if getattr(self.w, 'exportCheckBox' + formt).get():
				countFormats += 1
				self.w.run.enable(True)
				getattr(self.w, 'autohint' + formt).setAlpha(alphaActive)
				if 'Variable' not in formt:
					getattr(self.w, 'overlaps' + formt).setAlpha(alphaActive)
				if formt == 'WEB':
					getattr(self.w, 'outlines' + formt).setAlpha(alphaActive)
			else:
				getattr(self.w, 'autohint' + formt).setAlpha(alphaDeactivated)
				if 'Variable' not in formt:
					getattr(self.w, 'overlaps' + formt).setAlpha(alphaDeactivated)
				if formt == 'WEB':
					getattr(self.w, 'outlines' + formt).setAlpha(alphaDeactivated)
		
		if countFormats:
			self.w.run.enable(True)
		else:
			self.w.run.enable(False)
		

	def exportPathCallback(self, sender):
		newExportPath = GetFolder(message = 'Export to', allowsMultipleSelection = False)
		if newExportPath:
			self.exportPath = newExportPath
		self.w.exportPath.setTitle(self.exportPath)
		self.w.info.set('')


	def run(self, sender):
		# check if the export folder exists
		if not os.path.exists(self.exportPath):
			self.w.info.set('That folder doesn’t exist!')
			return

		# update the current default path
		Glyphs.defaults['OTFExportPath'] = self.exportPath

		# get fonts (all or the current one)
		fonts = Glyphs.fonts if self.w.exportAll.get() else [Glyphs.font]

		# if there are no fonts, notify about it
		if not fonts or None in fonts:
			self.w.info.set('Could not export: no fonts are open.')
			return

		# go
		for font in fonts:
			# set up progress bar and count instances and formats
			selectedFormats = [frmt for frmt in formats if getattr(self.w, 'exportCheckBox' + frmt).get()]
			activeInstances = [instance for instance in font.instances if instance.active and (Glyphs3 is False or (('Variable' in selectedFormats or 'Variable WEB' in selectedFormats) or instance.type != INSTANCETYPEVARIABLE))]
			totalCount = len(activeInstances) * sum(1 if frmt != 'WEB' else 2 for frmt in selectedFormats)
			currentCount = 0

			# get export path
			fontExportPath = self.exportPath + '/' + font.familyName if len(fonts) > 1 else self.exportPath

			# get family subfolders (will use if more than one)
			familyNames = []
			for instance in activeInstances:
				familyName = instance.customParameters['familyName'] if 'familyName' in instance.customParameters else font.familyName
				if familyName not in familyNames:
					familyNames.append(familyName)

			# create family subfolders
			if len(familyNames) > 1:
				for familyName in familyNames:
					if not os.path.exists(fontExportPath + '/' + familyName):
						os.makedirs(fontExportPath + '/' + familyName)

			# export
			for i, formt in enumerate(selectedFormats):
				# set up the file format and containers
				containers = [PLAIN] if 'WEB' not in formt else [WOFF, WOFF2]
				# frmt = (OTF if getattr(self.w, 'outlines' + formt).get() else TTF) if formt == 'WEB' else (OTF if i == 0 else TTF)
				
				if formt == 'WEB':
					frmt = OTF if getattr(self.w, 'outlines' + formt).get() else TTF
				elif 'Variable' in formt: # 'Variable' or 'Variable WEB'
					frmt = VARIABLE
				else:
					frmt = OTF if formt == 'OTF' else TTF

				# set up other options
				removeOverlap = getattr(self.w, 'overlaps' + formt).get() if 'Variable' not in formt else False
				autohint = getattr(self.w, 'autohint' + formt).get()

				# export each active instance
				for instance in activeInstances:
					# format is variable => skip non-variable instances
					if 'Variable' in formt:
						if Glyphs3 and instance.type != INSTANCETYPEVARIABLE:
							continue
					# format is not variable => skip variable instances
					elif Glyphs3 and instance.type == INSTANCETYPEVARIABLE:
						continue

					# get export path for one or multiple familyNames
					exportPath = fontExportPath
					if len(familyNames) > 1:
						familyName = instance.customParameters['familyName'] if 'familyName' in instance.customParameters else font.familyName
						exportPath = fontExportPath + '/' + familyName

					# get format subfolder
					if self.w.subfolders.get():
						if formt != 'Variable WEB':
							exportPath += '/' + formt + '/'
						else: # Put variable WEB into the variable folder
							exportPath += '/Variable/' 

					# create the folder if missing
					if not os.path.exists(exportPath):
						os.makedirs(exportPath)

					# export variable in Glyphs 2
					if formt == 'Variable' and Glyphs3 is False:
						font.export(FontPath = exportPath, Format = VARIABLE, AutoHint = autohint)
						break # only export for one instance

					# export the instance
					instance.generate(Format = frmt, FontPath = exportPath, Containers = containers, RemoveOverlap = removeOverlap, AutoHint = autohint)

					# update progress bar
					currentCount += len(containers)
					self.w.progress.set(100 / totalCount * currentCount)
					self.w.info.set('%s/%s  %s %s' %(currentCount, totalCount, formt, instance.name))
					
		# notification
		self.w.info.set('')
		Glyphs.showNotification('Export fonts', '%s was exported successfully.' % (font.familyName))

ExportToAllFormats()


	
	

