#MenuTitle: Rotate 45 CCW
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from math import sin, cos, pi, radians
__doc__="""
Rotates selected nodes and components.
"""

font = Glyphs.font
selectedLayer = font.selectedLayers[0]
selection = selectedLayer.selection
bounds = selectedLayer.selectionBounds

midX = bounds[0].x + bounds[1].width / 2
midY = bounds[0].y + bounds[1].height / 2
origin = ( midX, midY) # center of selection
angle = radians(45) # negative clockwise

def rotate ( origin, point, angle ):
	    
	    # Rotate a point counterclockwise by a given angle around a given origin.
	    # The angle should be given in radians.
	    
	    ox, oy = origin
	    px, py = point
	
	    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
	    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
	    return qx, qy


for element in selection:
	newX, newY = rotate (origin, (element.x, element.y), angle )
	
	if type(element) == GSComponent:
		
		# shift matrix
		shiftMatrix = [1, 0, 0, 1, -midX, -midY]
		element.applyTransform( shiftMatrix )
    	# rotate
		rotationMatrix = [ cos(-angle), -sin(-angle), sin(-angle), cos(-angle), 0, 0 ]
		element.applyTransform( rotationMatrix )
		# shift back
		shiftMatrix = [1, 0, 0, 1, midX, midY]
		element.applyTransform( shiftMatrix )

	else:
		element.x = newX 
		element.y = newY
