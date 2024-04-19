#MenuTitle: Align Top
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Aligns nodes and components to the bottom of the selection or nearest metrics.
"""
DIRECTION = 'Top' # either 'Top' or 'Bottom'
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

						newY = remap(node.y, currentY, line[-1].y, element.y, line[-1].y)
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
		descenderZone = layer.master.alignmentZoneForMetric_(layer.master.descender)
		baselineZone = layer.master.alignmentZoneForMetric_(0)
		xHeightZone = layer.master.alignmentZoneForMetric_(layer.master.xHeight)
		capHeightZone = layer.master.alignmentZoneForMetric_(layer.master.capHeight)
		ascenderZone = layer.master.alignmentZoneForMetric_(layer.master.ascender)
		# Known bug: special layers get zones from masters. Not sure how to access layer’s zones
	else: # Glyphs 3
		ascenderZone, capHeightZone, xHeightZone, baselineZone, descenderZone = layer.metrics
		ascender, capHeight, xHeight, baseline, descender = ascenderZone.position, capHeightZone.position, xHeightZone.position, baselineZone.position, descenderZone.position
	guides = [descender, 0, xHeight, capHeight, ascender, int(xHeight/2), int((xHeight + capHeight)/4), int(capHeight/2)]
	
	if descenderZone:
		guides.append(descender + descenderZone.size)
	if baselineZone:
		guides.append(baselineZone.size)
	if xHeightZone:
		guides.append(xHeight + xHeightZone.size)
	if capHeightZone:
		guides.append(capHeight + capHeightZone.size)
	if ascenderZone:
		guides.append(ascender + ascenderZone.size)
	guides.sort()
	

	if len(selection) == 1:
		# prev next oncurves as guides
		node = selection[0]
		try:
			guideNode = None
			if node.prevNode.type != 'offcurve':
				guideNode = node.prevNode
			elif node.prevNode.prevNode.prevNode != 'offcurve':
				guideNode = node.prevNode.prevNode.prevNode
			if guideNode and guideNode.y not in guides and node != guideNode:
				guides.append(guideNode.y)
		except: pass
		try:
			guideNode = None
			if node.nextNode.type != 'offcurve':
				guideNode = node.nextNode
			elif node.nextNode.nextNode.nextNode != 'offcurve':
				guideNode = node.nextNode.nextNode.nextNode
			if guideNode and guideNode.y not in guides and node != guideNode:
				guides.append(guideNode.y)
		except: pass
	guides.sort()

	# get closest guide and shiftY
	if DIRECTION == 'Bottom':
		currentY = layer.selectionBounds.origin.y
		closestGuide = guides[0]
	elif DIRECTION == 'Top':
		currentY = layer.selectionBounds.origin.y + layer.selectionBounds.size.height
		closestGuide = guides[-1]
	
	for guide in guides:
		if DIRECTION == 'Bottom':
			if guide < currentY and currentY - guide < currentY - closestGuide:
				closestGuide = guide
		elif DIRECTION == 'Top':
			if guide > currentY and guide - currentY < closestGuide - currentY:
				closestGuide = guide
				
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


def alignToSelection():
	for element in selection:
		# align components
		if type(element) == GSComponent:
			y = int(element.bounds.origin.y - element.y) # Glyphs 2 and 3 have different x y of components
			if DIRECTION == 'Bottom':
				element.y = layer.selectionBounds.origin.y - y
			elif DIRECTION == 'Top':
				element.y = layer.selectionBounds.origin.y + layer.selectionBounds.size.height - element.bounds.size.height - y

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
				if DIRECTION == 'Bottom':
					element.y = layer.selectionBounds.origin.y
				elif DIRECTION == 'Top':
					element.y = layer.selectionBounds.origin.y + layer.selectionBounds.size.height
				keepSmooth(element, currentY)

		# align anchors
		else:
			if DIRECTION == 'Bottom':
				element.y = layer.selectionBounds.origin.y
			elif DIRECTION == 'Top':
				element.y = layer.selectionBounds.origin.y + layer.selectionBounds.size.height
	# align paths
	if selectedPaths:
		for path in selectedPaths:
			if DIRECTION == 'Bottom':
				# get highest node in the path
				lowest = None
				for node in path.nodes:
					if lowest is None:
						lowest = node.y
					elif node.y < lowest:
						lowest = node.y
				shift = layer.selectionBounds.origin.y - lowest
			elif DIRECTION == 'Top':
				highest = None
				for node in path.nodes:
					if highest is None:
						highest = node.y
					elif node.y > highest:
						highest = node.y
				shift = layer.selectionBounds.origin.y + layer.selectionBounds.size.height - highest

			path.applyTransform((
					1,		# x scale factor
					0,		# x skew factor
					0,		# y skew factor
					1,		# y scale factor
					0,		# x position
					shift 	# y position
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
	alignToSelection()

# update metrics
layer.updateMetrics()




# smooth variations

	# possible combinations

	# OFFCURVE - smooth - offcurve
	# OFFCURVE - SMOOTH - offcurve
	# OFFCURVE - smooth - OFFCURVE
	# offcurve - SMOOTH - offcurve
	# offcurve - SMOOTH - OFFCURVE
	# offcurve - smooth - OFFCURVE

	# ONCURVE - smooth - offcurve
	# ONCURVE - SMOOTH - offcurve
	# ONCURVE - smooth - OFFCURVE
	# oncurve - SMOOTH - offcurve
	# oncurve - SMOOTH - OFFCURVE
	# oncurve - smooth - OFFCURVE

	# OFFCURVE - smooth - oncurve
	# OFFCURVE - SMOOTH - oncurve
	# OFFCURVE - smooth - ONCURVE
	# offcurve - SMOOTH - oncurve
	# offcurve - SMOOTH - ONCURVE
	# offcurve - smooth - ONCURVE

	# OFFCURVE - smooth - smooth - offcurve
	# OFFCURVE - SMOOTH - smooth - offcurve
	# OFFCURVE - SMOOTH - SMOOTH - offcurve
	# offcurve - SMOOTH - SMOOTH - OFFCURVE
	# offcurve - smooth - SMOOTH - OFFCURVE
	# offcurve - smooth - smooth - OFFCURVE

	# OFFCURVE - smooth - SMOOTH - offcurve
	# offcurve - SMOOTH - smooth - OFFCURVE
	# offcurve - smooth - SMOOTH - offcurve
	# offcurve - SMOOTH - smooth - offcurve



# align everything if:
	# more than 2 selected
	# OFFCURVE - SMOOTH - offcurve
	# offcurve - SMOOTH - OFFCURVE
	# OFFCURVE - smooth - OFFCURVE
	# ONCURVE - SMOOTH - offcurve
	# oncurve - SMOOTH - OFFCURVE
	# ONCURVE - smooth - OFFCURVE
	# OFFCURVE - SMOOTH - oncurve
	# offcurve - SMOOTH - ONCURVE
	# OFFCURVE - smooth - ONCURVE
	# OFFCURVE - SMOOTH - smooth - offcurve
	# OFFCURVE - SMOOTH - SMOOTH - offcurve
	# offcurve - SMOOTH - SMOOTH - OFFCURVE
	# offcurve - smooth - SMOOTH - OFFCURVE
	# OFFCURVE - smooth - SMOOTH - offcurve
	# offcurve - SMOOTH - smooth - OFFCURVE

# keep smooth if:
	# if line lenght 3 and one offcurve is not selected
	# OFFCURVE - smooth - offcurve
	# offcurve - smooth - OFFCURVE
	# ONCURVE - smooth - offcurve
	# offcurve - smooth - ONCURVE

	# offcurve - SMOOTH - oncurve
	# oncurve - SMOOTH - offcurve

# recalc Ys if:
	# if line lenght 3 and 1 oncurve is not selected or line lenght 4 and only 1 offcurve is selected
	# OFFCURVE - smooth - oncurve
	# oncurve - smooth - OFFCURVE
	# OFFCURVE - smooth - smooth - offcurve
	# offcurve - smooth - smooth - OFFCURVE


# push everything if:
	# only one node is selected and it's smooth and the other node is not non smooth offcurve
	# offcurve - SMOOTH - offcurve
	# offcurve - smooth - SMOOTH - offcurve
	# offcurve - SMOOTH - smooth - offcurve