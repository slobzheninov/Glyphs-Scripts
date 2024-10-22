#MenuTitle: Show All Layers
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Show all layers of the selected glyphs in a new tab
"""

from GlyphsApp import Glyphs, GSControlLayer

layers = Glyphs.font.selectedLayers
allLayers = []

# get all layers
for layer in layers:
	if not isinstance(layer, GSControlLayer):
		if layer.parent:
			for l in layer.parent.layers:
				allLayers.append(l)
			allLayers.append(GSControlLayer(10))  # newline

# append to a new tab
if allLayers:
	tab = Glyphs.font.newTab('')
	for layer in allLayers:
		tab.layers.append(layer)
