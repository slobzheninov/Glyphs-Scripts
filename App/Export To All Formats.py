#MenuTitle: Export To All Formats
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Export to all formats at once.
WEB formats are WOFF and WOFF2. If “PS outlines” is off, TT outlines will be exported for the web formats.
Compress OTF/TTF option converts exported OTF/TTF to web formats, which is faster than exporting them from Glyphs.
Optionally, separates formats into subfolders.
Instances with different familyNames go to different subfolders as well.
"""

import os, sys
from GlyphsApp import Glyphs, GetFolder, INSTANCETYPEVARIABLE, OTF, TTF, VARIABLE, PLAIN, WOFF, WOFF2
from vanilla import FloatingWindow, TextBox, CheckBox, SquareButton, Button, ProgressBar
try:
	from fontTools.ttLib import TTFont
	fontToolsImported = True
except:
	fontToolsImported = False



Glyphs.clearLog()
Glyphs3 = Glyphs.versionNumber >= 3

# window size and margin
M = 15
W, H = 380, M * 21
captionWidth = 130
columnWidth = 45
lineYs = [M, M * 3, M * 5, M * 7, M * 9, M * 11, M * 13, M * 15, M * 17, M * 19]  # y of each line (tittle, export, outline flavor, remove overlaps, autohint)
lineYs = [y - 7 for y in lineYs]  # shift all vertically a bit

captions = ['', 'Export', 'Autohint', 'Remove Overlaps', 'PS Outlines', 'Compress otf/ttf (faster)']
formats = ['OTF', 'TTF', 'WEB', 'Variable', 'VariableWEB']

# No Variable WEB in Glyphs 2
if Glyphs3 is False:
	formats.remove('VariableWEB')
	W -= columnWidth

alphaActive = 1
alphaDeactivated = .4


class CheckBoxWithAlpha(CheckBox):
	def setAlpha(self, value=1):
		self.getNSButton().setAlphaValue_(value)


class ExportToAllFormats():
	def __init__(self):
		self.exportPath = Glyphs.defaults['OTFExportPath']
		self.postProcessWEB = False
		self.postProcessVariableWEB = False

		# window
		self.w = FloatingWindow((W, H), 'Export to all formats')

		# make captions for each row
		for i in range(len(lineYs))[:6]:
			captionID = captions[i]
			caption = TextBox((M, lineYs[i], captionWidth*2, M), captions[i])
			setattr(self.w, captionID, caption)

		# make a column of options for each format
		for i in range(len(formats)):
			x = captionWidth + columnWidth * i
			if i > 2:
				x += 10  # add a gap to separate variable formats

			# format title
			formatTitle = formats[i] if i != 4 else 'WEB'  # shorten 'VariableWEB' to another 'WEB'
			y = lineYs[0]
			titleID = 'title' + formats[i]
			title = TextBox((x - columnWidth / 2, y, columnWidth * 2, M), formatTitle, alignment='center')
			setattr(self.w, titleID, title)

			x += columnWidth / 2 - 7
			# export checkbox
			y = lineYs[1]
			exportCheckBoxID = 'exportCheckBox' + formats[i]
			exportCheckBox = CheckBoxWithAlpha((x, y, columnWidth / 2, M), None, value=True, callback=self.checkBoxCallback)
			setattr(self.w, exportCheckBoxID, exportCheckBox)
			setattr(getattr(self.w, exportCheckBoxID), 'i', i)

			# autohint checkbox
			y = lineYs[2]
			autohintID = 'autohint' + formats[i]
			autohint = CheckBoxWithAlpha((x, y, columnWidth / 2, M), '', value=True)
			setattr(self.w, autohintID, autohint)

			# overlaps checkbox (except variable)
			if i < 3:
				y = lineYs[3]
				overlapsID = 'overlaps' + formats[i]
				overlaps = CheckBoxWithAlpha((x, y, columnWidth / 2, M), '', value=True)
				setattr(self.w, overlapsID, overlaps)

			# PS outlines (web only)
			if i == 2:
				y = lineYs[4]
				outlinesID = 'outlines' + formats[i]
				outlines = CheckBoxWithAlpha((x, y, columnWidth / 2, M), '')
				setattr(self.w, outlinesID, outlines)

			# post-process WEB
			if i in [2, 4]:
				y = lineYs[5]
				postProcessID = 'postProcess' + formats[i]
				postProcess = CheckBoxWithAlpha((x, y, columnWidth / 2, M), '', value=True, callback=self.checkBoxCallback)
				postProcess.ID = formats[i]
				setattr(self.w, postProcessID, postProcess)
				# disable checkbox if fontTools import failed
				if fontToolsImported is False:
					postProcess.enable(0)
					postProcess.setToolTip('FontTools library is missing. Install it in Plugin Manager → Modules')


		# Export Path
		self.w.exportPath = SquareButton((M + 3, lineYs[6], -M - 3, M), 'Export Path', callback=self.exportPathCallback)
		if self.exportPath:
			self.w.exportPath.setTitle(self.exportPath)

		# Export all open fonts
		self.w.exportAll = CheckBox((M, lineYs[7], W / 2, M), 'All open fonts')

		# Subfolders
		self.w.subfolders = CheckBox((W / 2, lineYs[7], W / 2, M), 'Format subfolders', value=True)

		# Run button
		self.w.run = Button((W / 2, lineYs[8], -M, M), 'Export', callback=self.run)
		if self.exportPath:
			self.w.exportPath.setTitle(self.exportPath)

		# progress bar
		self.w.progress = ProgressBar((M, H + 100, -M, M))

		# exporting instance
		self.w.info = TextBox((M, lineYs[9], -M, M), '')

		# Uncheck variable checkboxes by default
		for ID in ['exportCheckBoxVariable', 'exportCheckBoxVariableWEB']:
			checkbox = getattr(self.w, ID, None)
			if checkbox:
				checkbox.toggle()
				# self.checkBoxCallback(checkbox)
		# # toggle post-process checkbox
		self.checkBoxCallback(getattr(self.w, 'postProcessWEB'))
		self.checkBoxCallback(getattr(self.w, 'postProcessVariableWEB'))

		self.w.open()


	def checkBoxCallback(self, sender):
		# get ID (postProcess checkboxes’ ID is either 'WEB' or 'VariableWEB')
		ID = getattr(sender, 'ID', None)
		if ID:
			value = sender.get()
			if ID == 'VariableWEB':
				self.postProcessVariableWEB = value
				if self.w.exportCheckBoxVariableWEB.get():
					self.w.autohintVariableWEB.setAlpha(alphaDeactivated if value else alphaActive)
			else: # 'WEB'
				self.postProcessWEB = value
				if self.w.exportCheckBoxWEB.get():
					self.w.autohintWEB.setAlpha(alphaDeactivated if value else alphaActive)
					self.w.overlapsWEB.setAlpha(alphaDeactivated if value else alphaActive)

		countFormats = 0
		for formt in formats:
			alpha = alphaActive if getattr(self.w, 'exportCheckBox' + formt).get() else alphaDeactivated
			# add active formats to the counter
			if alpha == alphaActive:
				countFormats += 1

			if 'WEB' not in formt or (formt == 'VariableWEB' and not self.postProcessVariableWEB) or (formt == 'WEB' and not self.postProcessWEB):
				getattr(self.w, 'autohint' + formt).setAlpha(alpha)
			if 'Variable' not in formt and (formt != 'WEB' or not self.postProcessWEB):
				getattr(self.w, 'overlaps' + formt).setAlpha(alpha)
			if formt == 'WEB':
				getattr(self.w, 'outlines' + formt).setAlpha(alpha)
			if 'WEB' in formt:
				getattr(self.w, 'postProcess' + formt).setAlpha(alpha)

		# if WEB set to post-process mode, you can only choose outlines if both OTF/TTF set to export, otherwise it will compress the 1 available
		exportOTF = self.w.exportCheckBoxOTF.get()
		exportTTF = self.w.exportCheckBoxTTF.get()
		exportWEB = self.w.exportCheckBoxWEB.get()
		# WEB outlines
		alpha = alphaDeactivated
		if exportWEB and (exportOTF and exportTTF) or not self.postProcessWEB:
			alpha = alphaActive
			
		getattr(self.w, 'outlinesWEB').setAlpha(alpha)

		
		# deactivate run button if no formats are chosen for export		
		self.w.run.enable(countFormats > 0)
		

	def exportPathCallback(self, sender):
		newExportPath = GetFolder(message='Export to', allowsMultipleSelection=False)
		if newExportPath:
			self.exportPath = newExportPath
		self.w.exportPath.setTitle(self.exportPath)
		self.w.info.set('')

	def getAllFamilyNames(self, fonts, selectedFormats):
		familyNames = []
		for font in fonts:
			activeInstances = [instance for instance in font.instances if instance.active and (Glyphs3 is False or (('Variable' in selectedFormats or 'VariableWEB' in selectedFormats) or instance.type != INSTANCETYPEVARIABLE))]
			for instance in activeInstances:
				familyName = self.getFamilyNameForInstance(instance)
				if familyName not in familyNames:
					familyNames.append(familyName)
		return familyNames

	def createFolders(self, familyNames, selectedFormats):
		folders = {}
		for familyName in familyNames:

			# familyName path
			familyNamePath = self.exportPath + '/' + familyName if len(familyNames) > 1 else self.exportPath

			# format path
			for formt in selectedFormats:
				# format subfolders
				if self.w.subfolders.get():
					if formt != 'VariableWEB':
						formatPath = familyNamePath + '/' + formt + '/'
					else:  # Put VariableWEB into the variable folder
						formatPath = familyNamePath + '/Variable/'

					# create the format folder if missing
					if not os.path.exists(formatPath):
						os.makedirs(formatPath)

					# add path to dict
					if familyName not in folders:
						folders[familyName] = {}
					folders[familyName][formt] = formatPath

				# no format subfolders
				else:
					# create the familyName folder if missing
					if not os.path.exists(familyNamePath):
						os.makedirs(familyNamePath)

					# add path to dict
					if familyName not in folders:
						folders[familyName] = {}
					folders[familyName][formt] = familyNamePath
		return folders

	def getFamilyNameForInstance(self, instance):
		if 'familyName' in instance.customParameters:
			return instance.customParameters['familyName']
		elif Glyphs3 and instance.familyName:
			return instance.familyName
		else:
			return instance.font.familyName

	def exportInstances(self, fonts, selectedFormats, folders):
		for font in fonts:
			# set up the progress bar and count instances and formats
			activeInstances = [instance for instance in font.instances if instance.active and (Glyphs3 is False or (('Variable' in selectedFormats or 'VariableWEB' in selectedFormats) or instance.type != INSTANCETYPEVARIABLE))]

			# count formats and total fonts to export
			formatsCount = 0
			for frmt in selectedFormats:
				if frmt == 'WEB' and not self.postProcessWEB:
					formatsCount += 2
				elif frmt == 'VariableWEB' and not self.postProcessVariableWEB:
					formatsCount += 2
				elif 'WEB' not in frmt:
					formatsCount += 1
			totalCount = len(activeInstances) * formatsCount
			currentCount = 0

			# export
			for formt in selectedFormats:

				# skip WEB if it will be doen in post
				if formt == 'WEB' and self.postProcessWEB:
					continue
				if formt == 'VariableWEB' and self.postProcessVariableWEB:
					continue
				
				# get format
				if formt == 'OTF':
					frmt = OTF
				elif formt == 'TTF':
					frmt = TTF
				elif formt == 'WEB':
					frmt = OTF if getattr(self.w, 'outlines' + formt).get() else TTF
				else: # 'Variable' or 'VariableWEB'
					frmt = VARIABLE
				
				# get parameters
				containers = [PLAIN] if 'WEB' not in formt else [WOFF, WOFF2]
				removeOverlap = getattr(self.w, 'overlaps' + formt).get() if 'Variable' not in formt else False
				autohint = getattr(self.w, 'autohint' + formt).get()

				for instance in activeInstances:

					# format is variable => skip non-variable instances
					if 'Variable' in formt:
						if Glyphs3 and instance.type != INSTANCETYPEVARIABLE:
							continue
					# format is not variable => skip variable instances
					elif Glyphs3 and instance.type == INSTANCETYPEVARIABLE:
						continue

					# get familyName for instance
					familyName = self.getFamilyNameForInstance(instance)

					# get export path / folder
					try:
						exportPath = folders[familyName][formt]
						# check if the export folder exists
						if not os.path.exists(exportPath):
							print('Couldn’t find the folder for %s - %s - %s' % (familyName, instance.name, formt))
							Glyphs.showMacroWindow()
							return
					except:
						print('Couldn’t find the folder for %s - %s - %s' % (familyName, instance.name, formt))
						Glyphs.showMacroWindow()
						return

					# export variable in Glyphs 2
					if formt == 'Variable' and Glyphs3 is False:
						font.export(FontPath=exportPath, Format=VARIABLE, AutoHint=autohint)
						break  # only export for one instance

					# export the instance
					if Glyphs.versionNumber >= 3.3:
						instance.generate(format=frmt, fontPath=exportPath, containers=containers, removeOverlap=removeOverlap, autoHint=autohint)
					else:
						instance.generate(Format=frmt, FontPath=exportPath, Containers=containers, RemoveOverlap=removeOverlap, AutoHint=autohint)

					# update progress bar
					currentCount += len(containers)
					self.w.progress.set(100 / totalCount * currentCount)
					self.w.info.set('%s/%s  %s %s' % (currentCount, totalCount, formt, instance.name))
			Glyphs.showNotification('Export fonts', font.familyName + ' was exported successfully.')


	def compressFontsInFolder(self, sourcePath, exportPath, sourceFormats = ['.ttf']):
		list_ = os.listdir(sourcePath)
		# get files of the right extension
		sourceFiles = []
		for file_ in list_:
			name, ext = os.path.splitext(file_)
			if ext.lower() in sourceFormats:
				sourceFiles.append(file_)

		totalCount = len(sourceFiles)
		currentCount = 0

		for file_ in sourceFiles:
			fontPath = sourcePath + '/' + file_
			fontExportPath = exportPath + '/' + file_
			font = TTFont(fontPath)
			font.flavor = 'woff'
			font.save(fontExportPath.replace(ext, '.woff'))
			font.flavor = 'woff2'
			font.save(fontExportPath.replace(ext, '.woff2'))

			# update progress bar
			currentCount += 1
			self.w.progress.set(100 / totalCount * currentCount)
			self.w.info.set('%s/%s  %s %s' % (currentCount, totalCount, 'WEB compressing', file_))
		Glyphs.showNotification('Export fonts', 'Compressed successfully: ' + exportPath)


	def runPostProcessWEB(self, selectedFormats, folders):
		# compress OTF/TTF in the given folder if OTF/TTF are not exported (bonus)
		if len(selectedFormats) == 1 and 'WEB' in selectedFormats[0] and (self.postProcessWEB or self.postProcessVariableWEB):
			sourcePath = self.exportPath
			exportPath = sourcePath + '/WEB' if self.w.subfolders.get() else sourcePath
			self.compressFontsInFolder(sourcePath, exportPath, sourceFormats=['.otf', '.ttf'])

		# compress the exported files
		else:
			# get post process checkboxes
			for formt in selectedFormats:
				if self.postProcessWEB and formt == 'WEB':
					for familyName, formatSubfolders in folders.items():
						PSOutlines = getattr(self.w, 'outlines' + formt).get()
						sourceFormats =  ['.otf'] if PSOutlines else ['.ttf']
						sourcePath = formatSubfolders['OTF' if PSOutlines else 'TTF'] 
						exportPath = formatSubfolders['WEB']
						self.compressFontsInFolder(sourcePath, exportPath, sourceFormats)

				elif self.postProcessVariableWEB and formt == 'VariableWEB':
					for familyName, formatSubfolders in folders.items():
						sourceFormats = ['.ttf']
						sourcePath = formatSubfolders['Variable']
						exportPath = formatSubfolders['VariableWEB']
						self.compressFontsInFolder(sourcePath, exportPath, sourceFormats)

	def run(self, sender):
		# check if the export folder exists
		if not os.path.exists(self.exportPath):
			self.w.info.set('That folder doesn’t exist!')
			return

		# deactivate the run button to avoid accidental clicks
		self.w.run.enable(0)

		# update the current default path
		Glyphs.defaults['OTFExportPath'] = self.exportPath

		# get fonts (all or the current one)
		fonts = Glyphs.fonts if self.w.exportAll.get() else [Glyphs.font]

		# if there are no fonts, notify about it
		if not fonts or None in fonts:
			self.w.info.set('Could not export: no fonts are open.')
			return

		# get all selected formats from UI
		selectedFormats = [frmt for frmt in formats if getattr(self.w, 'exportCheckBox' + frmt).get()]

		# get familyNames from all fonts and all instances’ custom parameters
		familyNames = self.getAllFamilyNames(fonts, selectedFormats)

		# create folders
		folders = self.createFolders(familyNames, selectedFormats)

		# export instances
		self.exportInstances(fonts, selectedFormats, folders)

		# post process WEB
		self.runPostProcessWEB(selectedFormats, folders)

		# reset progress bar
		self.w.info.set('')
		
		# activate the run button back
		self.w.run.enable(1)

		return

ExportToAllFormats()