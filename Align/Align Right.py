#MenuTitle: Align Right
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the right of the selection.
"""

font = Glyphs.font
selectedLayer = font.selectedLayers[0]
selection = selectedLayer.selection
bounds = selectedLayer.selectionBounds

for element in selection:
	if type(element) == GSComponent:
		x = element.bounds[0].x - element.x # Glyphs 2 and 3 have different x y of components
		element.x = bounds[0].x + bounds[1].width - element.bounds[1].width - x
	else:
		element.x = bounds[0].x + bounds[1].width