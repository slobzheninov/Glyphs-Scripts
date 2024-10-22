#MenuTitle: G2 Harmonize
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from math import sqrt
from GlyphsApp import Glyphs
from Cocoa import NSPoint

# https://gist.github.com/simoncozens/3c5d304ae2c14894393c6284df91be5b source


Glyphs.clearLog()

font = Glyphs.font
layer = font.selectedLayers[0]


def getIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
	px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
	py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
	return (px, py)


def getDist(a, b):
	dist = sqrt((b.x - a.x)**2 + (b.y - a.y)**2)
	return dist


def remap(oldValue, oldMin, oldMax, newMin, newMax):
	try:
		oldRange = (oldMax - oldMin)
		newRange = (newMax - newMin)
		newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
		return newValue
	except:
		pass


if layer.selection:
	for node in layer.selection:
		if node.smooth and node.nextNode.type == 'offcurve' and node.prevNode.type == 'offcurve':
			P = node

			# find intersection of lines created by offcurves
			intersection = (getIntersection(P.nextNode.x, P.nextNode.y, P.nextNode.nextNode.x, P.nextNode.nextNode.y, P.prevNode.x, P.prevNode.y, P.prevNode.prevNode.x, P.prevNode.prevNode.y))
			d = NSPoint(intersection[0], intersection[1])

			# find ratios
			p0 = getDist(P.nextNode.nextNode, P.nextNode) / getDist(P.nextNode, d)
			p1 = getDist(d, P.prevNode) / getDist(P.prevNode, P.prevNode.prevNode)
			# ratio
			p = sqrt(p0 * p1)

			# set onpoint position based on that p ratio
			t = p / (p + 1)

			# oncurve
			P.x = remap(t, 0, 1, P.nextNode.x, P.prevNode.x)
			P.y = remap(t, 0, 1, P.nextNode.y, P.prevNode.y)

			# handles

			# deltaX = P.x - remap(t, 0, 1, P.nextNode.x, P.prevNode.x)
			# deltaY = P.y - remap(t, 0, 1, P.nextNode.y, P.prevNode.y)

			# P.nextNode.x += deltaX
			# P.nextNode.y += deltaY
			# P.prevNode.x += deltaX
			# P.prevNode.y += deltaY

			layer.updateMetrics()
