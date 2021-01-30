#MenuTitle: Dangerous Offcurves
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

# --------------------
# This script opens a new tab with layers if there are offcurve points
# closer to their curve segment than THRESHOLD VALUE
# --------------------



# --- c function from Glyphs to check line to curve intersection
from AppKit import NSBundle, NSPoint
bundle = NSBundle.bundleForClass_(GSFont.__class__)
objc.loadBundleFunctions(bundle, globals(), [("GSIntersectBezier3Line", b"@{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}")])
# intersections = GSIntersectBezier3Line(NSPoint(0, 0), NSPoint(10, 10), NSPoint(10, 30), NSPoint(0, 40), NSPoint(60, 20), NSPoint(-10000, 20))

Glyphs.clearLog()
font = Glyphs.font


# define how many units away can offcurve points be from the curve segment
# change this value if needed:
THRESHOLD = 0.05



def getHorizontalIntersection( point, a, b, c, d ): 
	try:
		# intersecting line
		e = NSPoint( -10000, point.y )
		f =	NSPoint( 10000, point.y )
		intersections = GSIntersectBezier3Line( a, b, c, d, e, f )
		intersection = intersections[0].pointValue()
		return intersection
	except:
		#print('Could not find horizontal intersection')
		return None
		
def getVerticalIntersection( point, a, b, c, d ): 
	try:		
		# intersecting line
		e = NSPoint( point.x, -10000 )
		f =	NSPoint( point.x, 10000 )
		intersections = GSIntersectBezier3Line( a, b, c, d, e, f )
		intersection = intersections[0].pointValue()
		return intersection
	except:
		#print('Could not find vertical intersection')
		return None

problematicLayers = []

# check in all glyphs
for glyph in font.glyphs:
	for layer in glyph.layers:
		for path in layer.paths:
			for node in path.nodes:
				# get curved segment
				if node.type == 'offcurve' and node.prevNode.type != 'offcurve':
					a = (node.prevNode.x, node.prevNode.y) 
					b = (node.x, node.y)
					c = (node.nextNode.x, node.nextNode.y) 
					d = (node.nextNode.nextNode.x, node.nextNode.nextNode.y)
					# get intersection points for two offcurves
					hIntersection1 = getHorizontalIntersection( node, a, b, c, d )
					vIntersection1 = getVerticalIntersection( node, a, b, c, d )
					hIntersection2 = getHorizontalIntersection( node.nextNode, a, b, c, d )
					vIntersection2 = getVerticalIntersection( node.nextNode, a, b, c, d )
					
					if hIntersection1 and vIntersection1 and hIntersection2 and vIntersection2:
						# if either offcurve point is closer to the curve than THRESHOLD value
						if (abs(hIntersection1.x - node.x) < THRESHOLD or
								abs(vIntersection1.y - node.y) < THRESHOLD or
								abs(hIntersection2.x - node.nextNode.x) < THRESHOLD or
								abs(vIntersection2.y - node.nextNode.y) < THRESHOLD):
							# collect layers
							if layer not in problematicLayers:
								problematicLayers.append( layer )
							print('%s -- %s' %(layer.parent.name, layer.name))

# open a new tab with potentially problematic layers
if problematicLayers:
	font.newTab( problematicLayers )
else:
	print('Could not find any offcurve points that are closer to their curves than %s units' %THRESHOLD)
			
