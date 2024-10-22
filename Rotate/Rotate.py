# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Rotates selected nodes and components.
"""

from math import sin, cos, radians

from GlyphsApp import Glyphs, GSComponent



def rotate(origin, point, angle):

	# Rotate a point counterclockwise by a given angle around a given origin.
	# The angle should be given in radians.

	ox, oy = origin
	px, py = point

	qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
	qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
	return qx, qy


def rotateLayer(angleDeg):
	font = Glyphs.font
	layer = font.selectedLayers[0]
	bounds = layer.selectionBounds

	midX = bounds[0].x + bounds[1].width / 2
	midY = bounds[0].y + bounds[1].height / 2
	origin = (midX, midY)  # center of selection
	angle = radians(angleDeg)  # negative clockwise
	selection = layer.selection

	for element in selection:
		newX, newY = rotate(origin, (element.x, element.y), angle)

		if isinstance(element, GSComponent):

			# shift matrix
			shiftMatrix = [1, 0, 0, 1, -midX, -midY]
			element.applyTransform(shiftMatrix)
			# rotate
			rotationMatrix = [cos(-angle), -sin(-angle), sin(-angle), cos(-angle), 0, 0]
			element.applyTransform(rotationMatrix)
			# shift back
			shiftMatrix = [1, 0, 0, 1, midX, midY]
			element.applyTransform(shiftMatrix)

		else:
			element.x = newX
			element.y = newY

	# update metrics
	layer.updateMetrics()
