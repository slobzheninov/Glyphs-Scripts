#MenuTitle: Point Counter
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Counts points in all layers of the selected glyphs and reports in macro panel.
"""

from GlyphsApp import Glyphs

font = Glyphs.font
Glyphs.clearLog()
Glyphs.showMacroWindow()


# Get selected glyph
for layer in font.selectedLayers:
	glyph = layer.parent
	print("---------- %s ----------" % glyph.name)

	incompatiblePaths = {}
	incompatibleOffcurves = {}
	incompatibleCurves = {}
	incompatibleLines = {}

	# count paths, on curve and off-curve points

	countPointsPrev1 = -1
	countPointsPrev2 = -1

	for layer in glyph.layers:
		countPaths = 0
		countOffcurves = 0
		countCurves = 0
		countLines = 0

		for i, path in enumerate(layer.paths):
			countPaths += 1
			for node in path.nodes:
				if node.type == "offcurve":
					countOffcurves += 1
				if node.type == "curve":
					countCurves += 1
				if node.type == "line":
					countLines += 1

		countPoints = countCurves + countOffcurves + countLines

		if countPoints == countPointsPrev1 or countPoints == countPointsPrev2 or countPointsPrev1 == -1:
			test = ""
		else:
			test = "? "

		countPointsPrev2 = countPointsPrev1
		countPointsPrev1 = countPoints

		print("%s%s points - %s lines, %s curves, %s offcurves, %s paths - %s" % (test, countPoints, countLines, countCurves, countOffcurves, countPaths, layer.name))
	print("")
