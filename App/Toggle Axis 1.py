#MenuTitle: Toggle Axis 1
# -*- coding: utf-8 -*-
__doc__="""
Toggles along masters across the 1st axis.
"""
from Foundation import NSUserDefaults, NSString

AXIS = 0	# in Python we count from 0


font = Glyphs.font


# Add axes property to layers
GSLayer.axes = property(lambda self: self.tempDataForKey_("axes"),
	lambda self, value: self.setTempData_forKey_(value, "axes"))


def getNextMaster(selectedLayer, relatedLayers):
	for layer in relatedLayers:
		if layer.axes[ AXIS ] > selectedLayer.axes[ AXIS ]:
			return layer
	return relatedLayers[0]


def getRelatedMasters(selectedMaster):
	# find "related" layers along the axis
	relatedMasters = []
	for master in font.masters:
		if master != selectedMaster:
			related = True
			for i, axis in enumerate( master.axes ):
				if i != AXIS:
					if axis != selectedMaster.axes[ i ]:
						related = False
			if related is True:
				relatedMasters.append( master )
	return relatedMasters


def toggleMaster(master):
	relatedMasters = getRelatedMasters(master)
	nextMaster = getNextMaster(master, relatedMasters)	

	tab = master.font.currentTab
	if tab:
		setMasterLayersToMaster(tab, newMaster = nextMaster, currentMaster = master)
	else:
		master.font.masterIndex = master.font.masters.index( nextMaster )


def setMaster(font, tab, textCursor, textRange, toggle, newMasterIndex):
	# select the layers
	tab.textCursor = textCursor
	tab.textRange = textRange
	# set master index
	font.masterIndex = newMasterIndex+toggle
	font.masterIndex -= toggle


def setMasterLayersToMaster(tab, newMaster, currentMaster=None):
	# get user's selection to reset later
	currentTextCursor = tab.textCursor
	currentTextRange = tab.textRange
	newMasterIndex = font.masters.index( newMaster )
	if currentMaster == None:
		currentMaster = newMaster
	# toggle master to some other master and back, otherwise it doesn't apply
	if newMaster == currentMaster:
		if 0 < newMasterIndex:
			toggle = -1
		else:
			toggle = 1
	else:
		toggle = 0

	# select old master layers and apply master
	textCursor = None
	textRange = 0
	for i, layer in enumerate(tab.layers):
		if layer.isMasterLayer and layer.master == currentMaster:
			if textCursor is None:
				textCursor = i
			textRange += 1
		else:
			if textCursor is not None:
				setMaster(font, tab, textCursor, textRange, toggle, newMasterIndex)
			# reset selection
			textCursor = None
			textRange = 0
	if textCursor is not None:
		setMaster(font, tab, textCursor, textRange, toggle, newMasterIndex)

	# set original user's selection
	tab.textCursor = currentTextCursor
	tab.textRange = currentTextRange


def getAxisValue(layer):
	return layer.axes[ AXIS ]


def getLayerAxes(layer):
	layerAxes = []
	if '{' in layer.name:
		axesStr = layer.name.replace('{', '').replace('}', '').replace(",", " ").split()
		for axis in axesStr:
			layerAxes.append(float(axis))
	else:
		layerAxes = layer.master.axes
	layer.axes = layerAxes
	return layerAxes


def getRelatedLayers(specialLayer):
	selectedLayerAxes = getLayerAxes(specialLayer)
	
	# ignore non {} layers
	if not selectedLayerAxes:
		return

	# get related layers
	relatedLayers = []
	for layer in specialLayer.parent.layers:

		# skip the layer itself
		if layer == specialLayer:
			continue

		# get layer axes
		layerAxes = getLayerAxes( layer )

		# check if all axes match (except for the AXIS)
		related = True
		for i, axis in enumerate( layerAxes ):
			if i != AXIS:
				if axis != specialLayer.axes[ i ]:
					related = False

		# append related layers
		if related is True:
			relatedLayers.append( layer )
	
	# sort by the AXIS value
	relatedLayers.sort( key = getAxisValue )
	return relatedLayers


def getNextSpecialLayerName(specialLayer):
	relatedLayers = getRelatedLayers(specialLayer)

	# {} layers
	if relatedLayers:
		nextSpecialLayer = getNextMaster(specialLayer, relatedLayers)
		return nextSpecialLayer.name

	# non {} layers
	else:
		return specialLayer.name


def getNextMasterId(masterId):
	master = font.masters[masterId]
	relatedMasters = getRelatedMasters(master)
	nextMaster = getNextMaster(master, relatedMasters)
	return nextMaster.id


def toggleMasterInTab(master, tab):
	# get next master for current master and save it	
	# go through each layer and if it’s different from master, find its next layer id, and save it too and swap.
	# in the line above also check in the list instead of finding again.

	cachedNextLayers = {}
	tempTabLayers = copy(tab.layers)

	# get next master to the tab master
	nextMasterId = getNextMasterId(master.id)
	nextMaster = font.masters[nextMasterId]

	# cache next master and toggle tab master
	cachedNextLayers[ master.id ] = nextMasterId
	master.font.masterIndex = master.font.masters.index( nextMaster )

	# get text selection
	selectionStart = tab.textCursor
	selectionEnd = tab.textCursor + tab.textRange

	# find layers different from tab master (check in the original/temp list)
	for i, layer in enumerate(tempTabLayers):

		# layer not selected (if any selection)
		if not (tab.textRange == 0   or   selectionStart <= i < selectionEnd or (selectionStart == selectionEnd and i == selectionStart)):
			continue

		# other master layer
		elif layer.isMasterLayer and layer.layerId != master.id:
			# get next layer (either from cache or do cache it)
			nextLayerId = cachedNextLayers.get( layer.layerId )
			if nextLayerId is None:
				nextLayerId = getNextMasterId( layer.layerId )
				cachedNextLayers[ layer.layerId ] = nextLayerId
			nextLayer = layer.parent.layers[ nextLayerId ]
			tempTabLayers[i] = nextLayer

		# special layer
		elif layer.isSpecialLayer:
			nextLayerName = cachedNextLayers.get( layer.name )
			if nextLayerName is None:
				nextLayerName = getNextSpecialLayerName(layer)
				cachedNextLayers[ layer.name ] = nextLayerName
			nextLayer = layer.parent.layers[ nextLayerName ]
			tempTabLayers[i] = nextLayer

		# control layer, skip
		elif type(selectedLayer) == GSControlLayer:
			continue

		# current master layer, just append
		else:
			tempTabLayers[i] = layer.parent.layers[ nextMasterId ]

	# apply new layers only if any differ from tab master OR if any selection
	if len(cachedNextLayers) > 1  or  0 < tab.textRange < len(tab.layers):
		tab.layers = tempTabLayers
		setMasterLayersToMaster(tab, nextMaster)



def getViewPortPosition(viewPort):
	viewPortX = viewPort.origin.x
	viewPortY = viewPort.origin.y
	return viewPortX, viewPortY


def setViewPortPosition(tab, viewPort, x, y):
	viewPort.origin.x = x
	viewPort.origin.y = y
	tab.viewPort = viewPort


def toggleAxis():
	tab = font.currentTab
	selectedMaster = font.selectedFontMaster

	if AXIS is None or AXIS >= len(font.axes):
		print("Axis %s not found" % AXIS)
		return

	if not tab:
		toggleMaster( selectedMaster )
	
	else:
		# get viewport position
		viewPort = tab.viewPort
		viewPortX, viewPortY = getViewPortPosition(viewPort)

		# toggle layers and masters
		toggleMasterInTab( selectedMaster, tab )

		# restore viewport position
		setViewPortPosition( tab, viewPort, viewPortX, viewPortY )


toggleAxis()