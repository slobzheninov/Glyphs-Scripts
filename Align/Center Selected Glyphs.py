#MenuTitle: Center Selected Glyphs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Makes equal left and right sidebearings for all layers in the selected glyphs.
"""

# Center selected glyphs

font = Glyphs.font

if font and font.selectedLayers:
	for selectedLayer in font.selectedLayers:
		glyph = selectedLayer.parent
		for layer in glyph.layers:
			width = layer.width
			sidebearings = layer.LSB + layer.RSB
			layer.LSB = int( sidebearings / 2 )
			layer.width = width	