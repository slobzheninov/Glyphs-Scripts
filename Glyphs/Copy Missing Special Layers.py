#MenuTitle: Copy Missing Special Layers
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Copies special layers from the 1st selected glyph to other selected glyphs (in a tab). 
Only copies layers that are missing in the target glyphs.
"""

Glyphs.clearLog()
if len(Font.selectedLayers) > 1:
	sourceGlyph = Font.selectedLayers[0].parent
	
	for l in Font.selectedLayers[1:]:
		destGlyph = l.parent
				
		for layer in sourceGlyph.layers:
			if layer.isSpecialLayer:
				
				# check if layer exists in target layer
				layerFound = False
				for layer2 in destGlyph.layers:
					if layer2.name == layer.name:
						layerFound = True

				if layerFound is False:
					newLayer = layer.copy()
					destGlyph.layers.append(newLayer)
					newLayer.reinterpolate()
					print('Copied layer: %s' % layer.name)