#MenuTitle: Overlap Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Select two tip nodes to move others to it – used for Right Grotesk special layers with overlaping nodes.
"""

from Foundation import NSPoint
from math import tan, radians
from GlyphsApp import Glyphs

font = Glyphs.font
layer = font.selectedLayers[0]
selection = layer.selection
italicAngle = layer.master.italicAngle


# from @mekkablue snippets
def italicize(thisPoint, italicAngle=0.0, pivotalY=0.0):  # don't change x to y for horizontal / vertical DIRECTION
	x = thisPoint.x
	yOffset = thisPoint.y - pivotalY  # calculate vertical offset
	italicAngle = radians(italicAngle)  # convert to radians
	tangens = tan(italicAngle)  # math.tan needs radians
	horizontalDeviance = tangens * yOffset  # vertical distance from pivotal point
	x += horizontalDeviance  # x of point that is yOffset from pivotal point
	return NSPoint(int(x), thisPoint.y)


# move on curves
for node in selection:
	if node.nextNode.type != 'offcurve' and node.nextNode.nextNode.type == 'offcurve':
		#  oncurve
		node.nextNode.x = node.x
		node.nextNode.y = node.y
		node.nextNode.smooth = False
		# offcurve
		node.nextNode.nextNode.x = italicize(NSPoint(node.x, node.nextNode.nextNode.y), italicAngle, node.y)[0]

	elif node.prevNode.type != 'offcurve' and node.prevNode.prevNode.type == 'offcurve':
		# oncurve
		node.prevNode.x = node.x
		node.prevNode.y = node.y
		node.prevNode.smooth = False
		# offcurve
		node.prevNode.prevNode.x = italicize(NSPoint(node.x, node.prevNode.prevNode.y), italicAngle, node.y)[0]
