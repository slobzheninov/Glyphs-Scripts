#MenuTitle: Align Vertical Center
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the vertical center of the selection or nearest metrics.
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

def keepSmooth(element, currentY):
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
			# unless they all have the same x
			for node in line:
				if node.selected or node.x != element.x:
					node.y = element.y
		
		# shift everything if only one node is selected and it's smooth and the other nodes are offcurves
		elif element.smooth and prev.type == 'offcurve' and next.type == 'offcurve':
			pass
			# for node in line:
			# 	if node != element:
			# 		node.y += (element.y - currentY)

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
		
		# otherwise adjust Y 
		else:
			for node in line:
				if node != line[0] and node != line[-1]:
					if element == line[0]:

						newY = remap(node.y, currentY, line[-1].y, element.y, line[-1].y) # doesn't work if y difference was 0
						node.y = newY
					elif element == line[-1]:
						newY = remap(node.y, currentY, line[0].y, element.y, line[0].y)
						node.y = newY

# from @mekkablue snippets
def italicize(thisPoint, italicAngle=0.0, pivotalY=0.0):
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
# get guides and alignment zones
	if Glyphs.versionNumber < 3: # Glyphs 2
		layerWidth, ascender, capHeight, descender, xHeight, italicAngle, unclear, midXheight = layer.glyphMetrics()
	else: # Glyphs 3
		ascenderZone, capHeightZone, xHeightZone, baselineZone, descenderZone = layer.metrics
		xHeight, capHeight = xHeightZone.position, capHeightZone.position

	# collect guides (mid xHeight, mid xHeight and capHeight, mid cap height)
	guides = [int(xHeight/2), int((xHeight + capHeight)/4), int(capHeight/2)]
	guides.sort()
	# get closest guide and shiftY
	currentY = layer.selectionBounds.origin.y + (layer.selectionBounds.size.height / 2)
	for i, guide in enumerate(guides):
		if currentY < guide:
			closestGuide = guide
			break
		elif currentY >= guides[-1]:
			closestGuide = guides[0]
	shiftY = closestGuide - currentY
	# align
	italicAngle = layer.italicAngle() if Glyphs.versionNumber < 3 else layer.italicAngle
	for node in selection:
		node.y += shiftY
		if italicAngle != 0:
			node.x = italicize(node, italicAngle, node.y-shiftY).x
	# keep smooth
	if len(selection) == 1:
		try:
			keepSmooth(selection[0], currentY)
		except: pass


def alignToSelectionCenter():
	selectionCenter = layer.selectionBounds.origin.y + layer.selectionBounds.size.height/2
	for element in selection:
		# align components
		if type(element) == GSComponent:
			y = int(element.bounds.origin.y - element.y) # Glyphs 2 and 3 have different x y of components
			element.y = selectionCenter - element.bounds.size.height/2 - y
		
		# align nodes
		elif type(element) == GSNode:
			align = True
			if selectedPaths:
				for path in selectedPaths:
					if element in path.nodes:
						align = False
						break

			if align is True:
				currentY = element.y
				element.y = selectionCenter
				keepSmooth(element, currentY)
		
		# align anchors
		else:
			element.y = selectionCenter

	# align paths
	if selectedPaths:
		for path in selectedPaths:
			pathCenter = path.bounds.origin.y + path.bounds.size.height/2
			shiftY = selectionCenter - pathCenter

			path.applyTransform((
					1,		# x scale factor
					0,		# x skew factor
					0,		# y skew factor
					1,		# y scale factor
					0,		# x position
					shiftY 	# y position
					))


# see if all selected points share Y coordinate
sameY = True
for element in selection:
	if element.y != selection[0].y:
		sameY = False
		break

# in caps lock mode, selection aligns to guides
cpsKeyFlag = 65536
cpsPressed = NSEvent.modifierFlags() & cpsKeyFlag == cpsKeyFlag

# if there’s only one element or path, align it to the guides
# or caps lock is on
if (len(selection) == 1 or
			sameY is True or
			(len(selectedPaths) == 1 and len(selection) == len(selectedPaths[0].nodes)) or
			cpsPressed):
	alignToGuides()

# if more than one element is selected
else:
	alignToSelectionCenter()

# update metrics
layer.updateMetrics()
