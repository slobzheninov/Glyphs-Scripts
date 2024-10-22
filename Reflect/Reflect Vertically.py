#MenuTitle: Reflect Vertically
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Flip selected nodes and components vertically.
"""

from GlyphsApp import Glyphs, GSComponent
font = Glyphs.font

layer = font.selectedLayers[0]
mid = layer.selectionBounds[0].y + layer.selectionBounds[1].height / 2

for element in layer.selection:
	element.y = mid - element.y + mid
	if isinstance(element, GSComponent):
		element.scale = (element.scale[0], -element.scale[1])

# update metrics
layer.updateMetrics()
