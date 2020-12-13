#MenuTitle: Align Bottom
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the bottom of the selection.
"""

font = Glyphs.font
selectedLayer = font.selectedLayers[0]
selection = selectedLayer.selection
bounds = selectedLayer.selectionBounds

for element in selection:
	if type(element) == GSComponent:
		y = element.bounds[0].y - element.y # Glyphs 2 and 3 have different x y of components
		element.y = bounds[0].y - y
	else:
		element.y = bounds[0].y
