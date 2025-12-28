#MenuTitle: Fit Zoom
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Fit the selected layer in the current tab on the screen. With Text tool on, fit the whole text by width.
"""

if Font and Font.currentTab and Layer:
	font = Font
	textTool = Glyphs.currentDocument.windowController().toolDrawDelegate().className() in ['GlyphsToolText', 'GlyphsToolHand']
	
	# Fit paragraph by width
	if textTool:

		# Adjust scale to fit paragraph by width with some margin
		tab = font.currentTab
		tab.scale *= (viewPort.size.width / tab.bounds.size.width * .95)
		font.parent.windowController().activeEditViewController().graphicView().updateBoundsFromFrameView()
		viewPort = tab.viewPort
		activePos = font.parent.windowController().activeEditViewController().graphicView().activePosition()

		# Margin
		M = (viewPort.size.width - tab.bounds.size.width) / 2

		# Set position
		minY = -viewPort.size.height + M
		maxY = -tab.bounds.size.height - M
		centerY = -viewPort.size.height/2 + activePos.y
		viewPort.origin.y = min(max(centerY, maxY), minY)
		viewPort.origin.x = -M

		# Apply position
		tab.viewPort = viewPort

	# Fit the selected layer on screen
	else:	
		font.parent.windowController().activeEditViewController().graphicView().zoomFitInWindow_(None)
		font.parent.windowController().activeEditViewController().graphicView().zoomOut_(None) # Add some margin
