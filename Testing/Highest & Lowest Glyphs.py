#MenuTitle: Highest & Lowest Glyphs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Finds tallest and lowest glyphs / Y coordinates.
"""

from GlyphsApp import Glyphs

maxY = None
minY = None
highest = None
lowest = None

font = Glyphs.font
for glyph in font.glyphs:
	for layer in glyph.layers:
		if not maxY or layer.bounds.origin.y + layer.bounds.size.height > maxY:
			maxY = layer.bounds.origin.y + layer.bounds.size.height
			highest = layer
		if not minY or layer.bounds.origin.y < minY:
			minY = layer.bounds.origin.y
			lowest = layer

print('highest: %s' % maxY)
print('lowest: %s' % minY)
font.newTab([highest, lowest])
