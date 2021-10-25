#MenuTitle: Kern to max
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
For the selected pair, sets the kerning value to maximum. Maximum is the half width of the narrower glyph in the pair.
"""


# set kerning to the maximum (half of the narrower glyph in the pair)

font = Glyphs.font

# get current pair
cursor = font.currentTab.textCursor
cachedGlyphs = font.parent.windowController().activeEditViewController().graphicView().layoutManager().cachedGlyphs()

# if at least two layers in the edit view
if cachedGlyphs and len(cachedGlyphs) > 1:
	leftLayer = cachedGlyphs[ cursor - 1 ]
	rightLayer = cachedGlyphs[ cursor ]

	# if both are master layers and the master is the same
	if leftLayer.isMasterLayer and rightLayer.isMasterLayer and leftLayer.master == rightLayer.master:
		master = leftLayer.master
		leftKey = leftLayer.parent.rightKerningKey
		rightKey = rightLayer.parent.leftKerningKey
		
		# kerning value is half width of the narrower layer in the pair
		if leftLayer.width < rightLayer.width:
			kerningValue = - int(leftLayer.width / 2)
		else:
			kerningValue = - int(rightLayer.width / 2)
		
		# set kerning
		font.setKerningForPair( master.id, leftKey, rightKey, kerningValue )