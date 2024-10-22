#MenuTitle: Fit Zoom
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Fit text in the current tab to full screen. Works weirdly in Glyphs 3.
"""

from GlyphsApp import Glyphs

Glyphs.clearLog()
font = Glyphs.font
tab = font.currentTab
viewPort = tab.viewPort

# check if text tool is selected
if Glyphs.currentDocument.windowController().toolDrawDelegate().className() in ['GlyphsToolText', 'GlyphsToolHand']:
	textTool = True
else:
	textTool = False


# text/hand tool > fit all
if textTool:
	# set scale to 1
	tab.scale = 1
	# set margin (relative)
	M = tab.bounds.size.width / 30
	# get screen ratio
	screenRatio = viewPort.size.width / viewPort.size.height
	# get text ratio
	textRatio = tab.bounds.size.width / tab.bounds.size.height

	# fit by width
	if textRatio > screenRatio:
		# width
		viewPort.size.width = tab.bounds.size.width + M * 2
		# x
		viewPort.origin.x = -M
		# y (centered)
		viewPort.origin.y = -viewPort.size.height / 2 - tab.bounds.size.height / 2

	# fit by height
	else:
		# height
		viewPort.size.height = tab.bounds.size.height + M * 2
		# y
		viewPort.origin.y = -tab.bounds.size.height
		# x (centered)
		viewPort.origin.x = -viewPort.size.width / 2 + tab.bounds.size.width / 2

	# apply changes
	tab.viewPort = viewPort


# other tools > fit current layer
else:
	if font.selectedLayers:
		# set scale to 1
		tab.scale = 1

		layer = font.selectedLayers[0]
		# get layer's origin position in tab
		activePos = font.parent.windowController().activeEditViewController().graphicView().activePosition()
		# set margin (absolute)
		M = 50
		# get screen ratio
		screenRatio = viewPort.size.width / viewPort.size.height
		# get current layer ratio (descender-ascender)
		layerHeight = abs(layer.master.descender) + layer.master.ascender
		textRatio = layer.width / layerHeight

		# # fit by width
		if textRatio > screenRatio:
			# width
			viewPort.size.width = layer.width + M * 2

		# fit by height
		else:
			# height
			viewPort.size.height = layerHeight + M * 2

		# x (centered)
		viewPort.origin.x = activePos.x - viewPort.size.width / 2 + layer.width / 2
		# y (centered)
		viewPort.origin.y = -viewPort.size.height / 2 + activePos.y + (layer.master.ascender + layer.master.descender) / 2

		# apply changes
		tab.viewPort = viewPort
