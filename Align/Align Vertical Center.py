#MenuTitle: Align Vertical Center
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the vertical center of the selection.
"""

font = Glyphs.font
selectedLayer = font.selectedLayers[0]
selection = selectedLayer.selection
bounds = selectedLayer.selectionBounds


for element in selection:
	if type(element) == GSComponent:
		y = element.bounds[0].y - element.y # Glyphs 2 and 3 have different x y of components
		element.y = bounds[0].y + bounds[1].height - bounds[1].height/2 - element.bounds[1].height/2 - y
	else:
		element.y = bounds[0].y + bounds[1].height - bounds[1].height/2
