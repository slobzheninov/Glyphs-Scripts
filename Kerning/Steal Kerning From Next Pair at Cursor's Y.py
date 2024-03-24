#MenuTitle: Steal kerning from next pair at cursor's Y
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from AppKit import NSPoint
__doc__="""
Copies kerning value from the next pair, as measured at the current cursor’s vertical position.
Example: to kern AV the same as VA, type AVVA, place cursor between AV, and point with the mouse where vertically you want to measure the distance.
"""
Glyphs.clearLog()
font = Glyphs.font

def getLayers(tab):
	try:
		textCursor = tab.textCursor	
		if textCursor == 0:
			return False
		layerA = tab.layers[textCursor-1]
		layerB = tab.layers[textCursor]
		layerC = tab.layers[textCursor+1]
		layerD = tab.layers[textCursor+2]
		# Check if all 4 are the same master layers
		if layerA.isMasterLayer and layerA.layerId == layerB.layerId == layerC.layerId == layerD.layerId:
			return layerA, layerB, layerC, layerD	
	except:
		return False


def getIntersection(layer, y, direction = 'left'):
	intersections = layer.calculateIntersectionsStartPoint_endPoint_decompose_(NSPoint(-10000, y), NSPoint(10000, y), True)[1:-1]
	if not intersections:
		return None
	if direction == 'left':
		return min(intersections, key=lambda point: point.x)
	else:
		return max(intersections, key=lambda point: point.x)


def getTotalDistance(layer1, layer2, y):
	try:
		# Get distance from the right most intersection to the right side in layer 1
		intersection1 = getIntersection(layer1, y, direction = 'right') 
		distance1 = layer1.width - intersection1.x

		# Get distance from the left most intersection to the left side in layer 2
		intersection2 = getIntersection(layer2, y, direction = 'left')
		distance2 = intersection2.x
		totalDistance = distance1 + distance2

		# Apply kerning, if any
		kerningValue = font.kerningForPair( layer1.layerId, layer1.parent.rightKerningKey, layer2.parent.leftKerningKey, direction = LTR )
		if not (kerningValue and kerningValue < 10000):
			kerningValue = 0

		return totalDistance, kerningValue
	except:
		return None, None

def getKerningKeys(layer1, layer2):
	# check exceptions
	if Glyphs.versionNumber < 3:
		exception1 = layer1.rightKerningExeptionForLayer_(layer2)
		exception2 = layer2.leftKerningExeptionForLayer_(layer1)
	else:
		exception1 = layer1.nextKerningExeptionForLayer_direction_(layer2, LTR)
		exception2 = layer2.previousKerningExeptionForLayer_direction_(layer1, LTR)
		
	# get kerning keys, either groups or exceptions
	rightKerningKey = layer1.parent.name if exception1 else layer1.parent.rightKerningKey
	leftKerningKey = layer2.parent.name if exception2 else layer2.parent.leftKerningKey
	return rightKerningKey, leftKerningKey

def applyKerning(masterId, rightKerningKey, leftKerningKey, value):
	if value:
		font.setKerningForPair(masterId, rightKerningKey, leftKerningKey, value)
	else:
		font.removeKerningForPair(masterId, rightKerningKey, leftKerningKey)

def stealKerning():
	# A tab must be open
	if not(font and font.currentTab):
		return

	# Get cursor’s Y
	cursorPosition = Glyphs.font.currentTab.graphicView().getActiveLocation_(Glyphs.currentEvent()) # NSPoint
	y = cursorPosition.y

	# Get layer pairs
	try:
		layerA, layerB, layerC, layerD = getLayers(font.currentTab)
	except:
		return

	# Get distances between pairs, including kerning
	totalDistance1, kerningValue1 = getTotalDistance(layerA, layerB, y)
	totalDistance2, kerningValue2 = getTotalDistance(layerC, layerD, y)

	# Get difference
	if totalDistance1 and totalDistance1:
		kerningValue = int(totalDistance2 - totalDistance1 + kerningValue2)
	else:
		print('Could not steal kerning from the next pair: failed to measure the distance at the cursor’s vertical position %s.' % int(y))
		return

	# Apply kerning
	rightKerningKey, leftKerningKey = getKerningKeys(layerA, layerB)
	applyKerning(layerA.associatedMasterId, rightKerningKey, leftKerningKey, kerningValue)

	# Report
	print('Stole kerning %s for %s %s measuring it from %s %s at y=%s' % (kerningValue, rightKerningKey.replace('@MMK_L_', '@'), leftKerningKey.replace('@MMK_R_', '@'), layerC.parent.name, layerD.parent.name, int(y)))
	print('Master: %s' % layerA.name)

stealKerning()