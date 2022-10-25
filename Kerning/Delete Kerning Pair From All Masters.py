#MenuTitle: Delete Kerning Pair From All Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Deletes kerning for the selected pair(s) from all masters.
"""

font = Glyphs.font

def removeKerning( leftLayer, rightLayer ):
	# if both are master layers and the master is the same
	if leftLayer.isMasterLayer and rightLayer.isMasterLayer and leftLayer.master == rightLayer.master:
		# master = leftLayer.master
		leftKey = leftLayer.parent.rightKerningKey
		rightKey = rightLayer.parent.leftKerningKey
		
		# set kerning
		for master in font.masters:
			font.removeKerningForPair( master.id, leftKey, rightKey, direction=LTR)


# more than 2 layers selected
if len(font.selectedLayers) > 2:
	for i, layer in enumerate(font.selectedLayers):
		
		# unless it's the last layer
		if i < len( font.selectedLayers)-1:
			leftLayer = layer
			rightLayer = font.selectedLayers[ i+1 ]

			removeKerning( leftLayer, rightLayer )


# no selection (current pair)
else:
	# get current pair
	cursor = font.currentTab.textCursor
	# Glyphs 2
	if Glyphs.versionNumber < 3: 
		cachedGlyphs = font.parent.windowController().activeEditViewController().graphicView().layoutManager().cachedGlyphs()
	# Glyphs 3
	else:							
		cachedGlyphs = font.parent.windowController().activeEditViewController().graphicView().layoutManager().cachedLayers()

	# if at least two layers in the edit view
	if cachedGlyphs and len(cachedGlyphs) > 1:
		leftLayer = cachedGlyphs[ cursor - 1 ]
		rightLayer = cachedGlyphs[ cursor ]

		removeKerning( leftLayer, rightLayer )



