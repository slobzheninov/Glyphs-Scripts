#MenuTitle: Export To All Formats
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Export to all formats at once.
WEB formats are WOFF and WOFF2. If “PS outlines” is off, TT outlines will be exported for the web formats.
“All open fonts” will export all fonts currently open in Glyphs; otherwise, only currently active one will be exported.
“Format subfolders” checkbox splits all formats to subfolders.
Doesn’t export variable.
"""

from vanilla import FloatingWindow, TextBox, PopUpButton, CheckBox, SquareButton, Button, ProgressBar
import os

Glyphs.clearLog()


# window size and margin
W, H = 310, 300
M = 18
captionWidth = 140
columnWidth = 50
lineYs = [ M, M*2.5, M*4, M*5.5, M*7, M*9, M*11, M*13, M*15 ] # y of each line (tittle, export, outline flavor, remove overlaps, autohint)
captions = [ '', 'Export', 'Remove Overlaps', 'Autohint', 'PS Outlines' ]
formats = ['OTF', 'TTF', 'WEB']

alphaActive = 1
alphaDeactivated = .4




class CheckBoxWithAlpha( CheckBox ):
	def setAlpha( self, value = 1 ):
		self.getNSButton().setAlphaValue_( value )


class ExportToAllFormats():

	def __init__( self ):

		self.exportPath = Glyphs.defaults["OTFExportPath"]
		
		# window
		self.w = FloatingWindow((W, H), 'Export to all formats')

		# make captions for each row
		for i in range(len(lineYs))[:5]:
			captionID = captions[i]
			caption = TextBox((M, lineYs[i], captionWidth, M), captions[i])
			setattr( self.w, captionID, caption )


		# make a column of options for each format
		for i in range(len(formats)):
			x = captionWidth + i*columnWidth

			# format title
			y = lineYs[0]
			titleID = 'title' + formats[i]
			title = TextBox((x, y, columnWidth, M), formats[i], alignment = 'center')
			setattr( self.w, titleID, title )

			x = x+columnWidth/2-7
			# export checkbox
			y = lineYs[1]
			exportCheckBoxID = 'exportCheckBox' + formats[i]
			exportCheckBox = CheckBox((x, y, columnWidth, M), None, value=True, callback = self.exportCheckBoxCallback)
			setattr( self.w, exportCheckBoxID, exportCheckBox )
			setattr( getattr( self.w, exportCheckBoxID ), 'i', i )

			# overlaps checkbox
			y = lineYs[2]
			overlapsID = 'overlaps' + formats[i]
			overlaps = CheckBoxWithAlpha((x, y, columnWidth, M),'', value=True)
			setattr( self.w, overlapsID, overlaps )

			# autohint checkbox
			y = lineYs[3]
			autohintID = 'autohint' + formats[i]
			autohint = CheckBoxWithAlpha((x, y, columnWidth, M),'', value=True)
			setattr( self.w, autohintID, autohint )

			# PS outlines (web only)
			if i == 2:
				y = lineYs[4]
				outlinesID = 'outlines' + formats[i]
				outlines = CheckBoxWithAlpha((x, y, columnWidth, M),'')
				setattr( self.w, outlinesID, outlines )

		# Export Path
		self.w.exportPath = SquareButton((M+3, lineYs[5], -M-3, M), 'Export Path', callback = self.exportPathCallback)
		if self.exportPath:
			self.w.exportPath.setTitle( self.exportPath )

		# Export all open fonts
		self.w.exportAll = CheckBox((M, lineYs[6], W/2, M), 'All open fonts')

		# Subfolders
		self.w.subfolders = CheckBox((W/2, lineYs[6], W/2, M), 'Format subfolders', value=True)
		
		# Run button
		self.w.run = Button((W/2, lineYs[7], -M, M), 'Export', callback = self.run)
		if self.exportPath:
			self.w.exportPath.setTitle( self.exportPath )

		# progress bar
		self.w.progress = ProgressBar((M, H+100, -M, M))

		# importing instance
		self.w.info = TextBox((M, lineYs[8], -M, M), '')
		self.w.open()


	def exportCheckBoxCallback( self, sender ):
		# deactivate run button if no formats are chosen for export
		countFormats = 0
		for formt in formats:
			if getattr( self.w, 'exportCheckBox' + formt).get():
				countFormats += 1
				self.w.run.enable( True )
				getattr( self.w, 'overlaps' + formt).setAlpha( alphaActive )
				getattr( self.w, 'autohint' + formt).setAlpha( alphaActive )
				if formt == 'WEB':
					getattr( self.w, 'outlines' + formt).setAlpha( alphaActive )
			else:
				getattr( self.w, 'overlaps' + formt).setAlpha( alphaDeactivated )
				getattr( self.w, 'autohint' + formt).setAlpha( alphaDeactivated )
				if formt == 'WEB':
					getattr( self.w, 'outlines' + formt).setAlpha( alphaDeactivated )
		
		if countFormats:
			self.w.run.enable( True )
		else:
			self.w.run.enable( False )
		

	def exportPathCallback( self, sender ):
		newExportPath = GetFolder(message="Export to", allowsMultipleSelection = False)
		if newExportPath:
			self.exportPath = newExportPath
		self.w.exportPath.setTitle( self.exportPath )
		self.w.info.set('')


	def run( self, sender ):
		# if export folder does not exist, warn about it
		if not os.path.exists( self.exportPath ):
			self.w.info.set('That folder does’t exist!')
			return

		# update current default path
		Glyphs.defaults["OTFExportPath"] = self.exportPath

		# get fonts (all or current one)
		if self.w.exportAll:
			fonts = Glyphs.fonts
		else:
			fonts = [Glyphs.font]

		# go
		for font in fonts:
			# if there's no font, notify about it
			if font is None:
				self.w.info.set( 'Seems like no fonts are open.' )
				return
			
			# progress bar setup
			currentCount = 0
			instancesCount = 0
			for instance in font.instances:
				# ignore variable
				if Glyphs.versionNumber >= 3 and instance.type == INSTANCETYPEVARIABLE:
					continue
				if instance.active:
					instancesCount += 1
			formatsCount = 0
			for formt in formats:
				if getattr( self.w, 'exportCheckBox' + formt).get():
					formatsCount += 1
					if formt == 'WEB':
						formatsCount += 1 # woff + woff2
			totalCount = instancesCount * formatsCount


			# export
			for i, formt in enumerate(formats):

				if getattr( self.w, 'exportCheckBox' + formt).get():
					# file format
					# otf/ttf
					if i < 2:
						containers = [PLAIN]
					# web
					else:
						containers = [WOFF, WOFF2]

					# format
					if i == 0: 
						frmt = OTF
					elif i == 1:
						frmt = TTF
					elif i == 2:
						if getattr( self.w, 'outlines' + formt).get():
							frmt = OTF
						else:
							frmt = TTF

					# remove overlap
					removeOverlap = getattr( self.w, 'overlaps' + formt).get()

					# autohint
					autohint = getattr( self.w, 'autohint' + formt).get()

					# export destination
					exportPath = self.exportPath
					# # if path does not exist, warn about it
					# if not os.path.exists( exportPath ):
					# 	self.w.info.set('That folder does’t exist!')
					# 	return

					# add font subfolder, if all exporting
					if len(fonts) > 1:
						exportPath += '/' + font.familyName

					# add subfolders
					if self.w.subfolders.get():
						exportPath += '/' + formt + '/'
						# create folder if it doesn't exist
						if not os.path.exists( exportPath ):
							os.makedirs( exportPath )

					for instance in font.instances:
						# ignore variable
						if Glyphs.versionNumber >= 3 and instance.type == INSTANCETYPEVARIABLE:
							continue
						if instance.active:
							instance.generate( Format = frmt, FontPath = exportPath, Containers = containers, RemoveOverlap = removeOverlap, AutoHint = autohint)

							# update progress bar
							currentCount += len(containers)
							self.w.progress.set(100/totalCount*currentCount)
							self.w.info.set( '%s/%s  %s %s' %(currentCount, totalCount, formt, instance.name ))


						
			# notification
			self.w.info.set('')
			Glyphs.showNotification('Export fonts', '%s was exported successfully.' % (font.familyName))

		

		
		


ExportToAllFormats()


	
	