#MenuTitle: Align Horizontal Center
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the horizontal center of the selection or nearest metrics.
"""
from math import radians, tan
from Foundation import NSPoint, NSEvent

def remap(oldValue, oldMin, oldMax, newMin, newMax):
	try:
		oldRange = (oldMax - oldMin)  
		newRange = (newMax - newMin)  
		newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
		return newValue
	except:
		return None

def getSmoothLine(element, prev, prevPrev, prevPrevPrev, next, nextNext, nextNextNext):
	# get the smooth line of nodes
	line = []

	if element.smooth:
		# 4 nodes line
		if prev.smooth or next.smooth: 
			if prev.smooth:
				line = [prevPrev, prev, element, next]
			elif next.smooth:
				line = [prev, element, next, nextNext]
		# 3 nodes line
		else:
			line = [prev, element, next]
	
	elif prev.smooth:
		if prevPrev.smooth:
			line = [prevPrevPrev, prevPrev, prev, element]
		else:
			line = [prevPrev, prev, element]
	elif next.smooth:
		if nextNext.smooth:
			line = [nextNextNext, nextNext, next, element]
		else:
			line = [nextNext, next, element]
	return line

def keepSmooth(element, currentX):
	try:
		prev, prevPrev, prevPrevPrev = element.prevNode, element.prevNode.prevNode, element.prevNode.prevNode.prevNode
		next, nextNext, nextNextNext = element.nextNode, element.nextNode.nextNode, element.nextNode.nextNode.nextNode
		line = getSmoothLine(element, prev, prevPrev, prevPrevPrev, next, nextNext, nextNextNext)
		selectedInLine = []
	except:
		line = []
	
	if line:
		for node in line:
			if node.selected:
				selectedInLine.append(node)

		# align everything if more than 2 nodes in line are selected
		if len(selectedInLine) > 1:
			# unless they all have the same y
			for node in line:
				if node.selected or node.y != element.y:
					node.x = element.x
		
		# shift everything if only one node is selected and it's smooth and the other nodes are offcurves
		elif element.smooth and prev.type == 'offcurve' and next.type == 'offcurve':
			pass
			# for node in line:
			# 	if node != element:
			# 		node.x += (element.x - currentX)

		# keep smooth if line len == 3 and one offcurve is not selected
		elif (len(line) == 3  and
				((line[0].type == 'offcurve' and line[0].selected is False) or
				 (line[2].type == 'offcurve' and line[2].selected is False))):
			if (line[0].type == 'offcurve' and line[0].selected is False):
				element.parent.setSmooth_withCenterNode_oppositeNode_(line[0], line[1], line[2])
			else:
				element.parent.setSmooth_withCenterNode_oppositeNode_(line[2], line[1], line[0])
		
		# keep smooth if line len == 4 and only one oncurve is selected
		elif (len(line) == 4 and
				len(selectedInLine) == 1):
			if line[1].selected or line[2].selected:
				element.parent.setSmooth_withCenterNode_oppositeNode_(line[0], line[1], line[2])
				element.parent.setSmooth_withCenterNode_oppositeNode_(line[3], line[2], line[1])	
		
		# otherwise adjust X
		else:
			for node in line:
				if node != line[0] and node != line[-1]:
					if element == line[0]:

						newX = remap(node.x, currentX, line[-1].x, element.x, line[-1].x)
						node.x = newX
					elif element == line[-1]:
						newX = remap(node.x, currentX, line[0].x, element.x, line[0].x)
						node.x = newX

# from @mekkablue snippets
def italicize(thisPoint, italicAngle=0.0, pivotalY=0.0): # don't change x to y for horizontal / vertical DIRECTION
	x = thisPoint.x
	yOffset = thisPoint.y - pivotalY # calculate vertical offset
	italicAngle = radians(italicAngle) # convert to radians
	tangens = tan(italicAngle) # math.tan needs radians
	horizontalDeviance = tangens * yOffset # vertical distance from pivotal point
	x += horizontalDeviance # x of point that is yOffset from pivotal point
	return NSPoint(int(x), thisPoint.y)


# ----------------------------------------


layer = Font.selectedLayers[0]
selection = layer.selection

def getSelectedPaths():
	selectedPaths = []
	for path in layer.paths:
		if path.selected:
			selectedPaths.append(path)
	return selectedPaths
selectedPaths = getSelectedPaths()


def alignToGuides():
	# collect guides
	guides = [int(layer.width/2)]
	guides.sort()

	# check italic
	italicAngle = layer.italicAngle() if Glyphs.versionNumber < 3 else layer.italicAngle
	if italicAngle != 0:
		# italicize guides
		italicGuides = []
		for guide in guides:
			italicGuide = italicize(NSPoint(guide, 0), italicAngle, layer.master.xHeight/2)[0]
			italicGuides.append(italicGuide)
		italicGuides.sort()
		guides = italicGuides
		
		# < backslant layer
		ySkew = tan(radians(italicAngle))
		layer.applyTransform ((
				1.0, 	# x scale factor
				0.0,	# x skew factor
				-ySkew, # y skew factor
				1.0, 	# y scale factor
				0.0,	# x position
				0.0  	# y position
				))	

	# get closest guide and shiftX
	currentX = layer.selectionBounds.origin.x + (layer.selectionBounds.size.width / 2)
	for i, guide in enumerate(guides):
		if currentX < guide:
			closestGuide = guide
			break
		elif currentX >= guides[-1]:
			closestGuide = guides[0]
	shiftX = closestGuide - currentX
	
	# align to the guide
	italicAngle = layer.italicAngle() if Glyphs.versionNumber < 3 else layer.italicAngle
	for element in selection:
		element.x += shiftX
	
	# set smooth
	if len(selection) == 1:
		try:
			keepSmooth(selection[0], currentX)
		except: pass

	# if italic, slant back
	if italicAngle != 0:
		ySkew = tan(radians(italicAngle))
		layer.applyTransform ((
				1.0, 	# x scale factor
				0.0,	# x skew factor
				ySkew, 	# y skew factor
				1.0, 	# y scale factor
				0.0,	# x position
				0.0  	# y position
				))


def alignToSelectionCenter():
	selectionCenter = layer.selectionBounds.origin.x + layer.selectionBounds.size.width/2
	for element in selection:
		# align components
		if type(element) == GSComponent:
			x = element.bounds.origin.x - element.x # Glyphs 2 and 3 have different x y of components
			element.x = selectionCenter - element.bounds.size.width/2 - x
		
		# align nodes
		elif type(element) == GSNode:
			align = True
			if selectedPaths:
				for path in selectedPaths:
					if element in path.nodes:
						align = False
						break

			if align is True:
				currentX = element.x
				element.x = selectionCenter
				keepSmooth(element, currentX)
		
		# align anchors
		else:
			element.x = selectionCenter

	# align paths
	if selectedPaths:
		for path in selectedPaths:
			pathCenter = path.bounds.origin.x + path.bounds.size.width/2
			shiftX = selectionCenter - pathCenter
			
			path.applyTransform((
					1,		# x scale factor
					0.0,		# x skew factor
					0.0,		# y skew factor
					1,		# y scale factor
					shiftX,	# x position
					0 		# y position
					))


# see if all selected points share Y coordinate
sameX = True
for element in selection:
	if element.x != selection[0].x:
		sameX = False
		break

# in caps lock mode, selection aligns to guides
cpsKeyFlag = 65536
cpsPressed = NSEvent.modifierFlags() & cpsKeyFlag == cpsKeyFlag

# if there’s only one element or path, align it to the guides
# or caps lock is on
if (len(selection) == 1 or
			sameX is True or
			(len(selectedPaths) == 1 and len(selection) == len(selectedPaths[0].nodes)) or
			cpsPressed):
	alignToGuides()

# if more than one element is selected
else:
	alignToSelectionCenter()

# update metrics
layer.updateMetrics()
