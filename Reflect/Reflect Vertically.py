#MenuTitle: Reflect Vertically
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Reflects nodes vertically.
"""

font = Glyphs.font
layer = font.layer[0]
selection = layer.selection
bounds = layer.selectionBounds
mid = bounds[0].y + bounds[1].height / 2

for element in selection:
	if type(element) == GSComponent:
		y = element.bounds[0].y - element.y # Glyphs 2 and 3 have different y y of components
		element.y = mid + (mid - element.y)
		if Glyphs.versionNumber >= 3:
			element.scale = (1, -element.scale[1])
		else:
			element.scale = (1, -1)
	else:
		element.y = mid + (mid - element.y)

# update metrics
layer.updateMetrics()

Glyphs.clearLog()