#MenuTitle: Reflect Horizontally
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Reflects nodes horizontally.
"""

font = Glyphs.font
layer = font.selectedLayers[0]
selection = layer.selection
bounds = layer.selectionBounds
mid = bounds[0].x + bounds[1].width / 2

for element in selection:
	if type(element) == GSComponent:
		x = element.bounds[0].x - element.x # Glyphs 2 and 3 have different x y of components
		element.x = mid + (mid - element.x)
		if Glyphs.versionNumber >= 3:
			element.scale = (-element.scale[0], 1)
		else:
			element.scale = (-1, 1)
	else:
		element.x = mid + (mid - element.x)

# update metrics
layer.updateMetrics()

Glyphs.clearLog()