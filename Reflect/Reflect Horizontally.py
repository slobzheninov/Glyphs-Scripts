#MenuTitle: Reflect Horizontally
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Flip selected nodes and components horizontally.
"""

layer = Glyphs.font.selectedLayers[0]
mid = layer.selectionBounds[0].x + layer.selectionBounds[1].width / 2

for element in layer.selection:
	element.x = mid - element.x + mid
	if type(element) == GSComponent:
		element.scale = (-element.scale[0], element.scale[1])

# update metrics
layer.updateMetrics()