#MenuTitle: Toggle Axis 4
# -*- coding: utf-8 -*-
__doc__="""
Toggles along masters across the 4th axis.
"""
from Foundation import NSUserDefaults, NSString
Glyphs.clearLog()


AXIS = 3	# in Python we count from 0


# Add axes property to layers
GSLayer.axes = property(lambda self: self.tempDataForKey_("axes"),
	lambda self, value: self.setTempData_forKey_(value, "axes"))

def getLayerAxes(layer):
	layerAxes = []
	if layer.isSpecialLayer and '{' in layer.name:
		axesStr = layer.name.replace('{', '').replace('}', '').replace(",", " ").split()
		for axis in axesStr:
			layerAxes.append(float(axis))
	else:
		layerAxes = layer.master.axes
	return layerAxes

def getAxisValue(layer):
	  return layer.axes[ AXIS ]

def getRelatedLayers(selectedLayer):
	selectedLayer.axes = getLayerAxes(selectedLayer)
	relatedLayers = []

	for layer in selectedLayer.parent.layers:
		# skip the layer itself
		if layer == selectedLayer:
			continue
		related = True
		# get layer axes
		layer.axes = getLayerAxes( layer )
		for i, axis in enumerate( layer.axes ):
			if i != AXIS:
				if axis != selectedLayer.axes[ i ]:
					related = False
		# append related layers
		if related is True:
			relatedLayers.append( layer )
	
	# sort by the AXIS value
	relatedLayers.sort( key = getAxisValue )
	return relatedLayers


def getNextLayer(selectedLayer, relatedLayers):
	for layer in relatedLayers:
		if layer.axes[ AXIS ] > selectedLayer.axes[ AXIS ]:
			return layer
	return relatedLayers[0]


def getRelatedMasters(selectedMaster):
	# find "related" layers along the axis
	relatedMasters = []
	for master in selectedMaster.font.masters:
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
	nextMaster = getNextLayer(master, relatedMasters)	

	tab = master.font.currentTab
	if tab:
		setMasterLayersToMaster(tab, newMaster = nextMaster, currentMaster = master)
	else:
		master.font.masterIndex = master.font.masters.index( nextMaster )


def getAllNextLayers(selectedLayers):
	# get related layers for selected layers
	allNextLayers = {}
	for selectedLayer in selectedLayers:
		selectedLayer.axes = getLayerAxes(selectedLayer)
		ID = str(selectedLayer.axes)
		if ID not in allNextLayers:
			relatedLayers = getRelatedLayers(selectedLayer)
			nextLayer = getNextLayer(selectedLayer, relatedLayers)
			allNextLayers[ID] = nextLayer.axes
	return allNextLayers


def getLayerForAxes(axes, selectedLayer):
	for layer in selectedLayer.parent.layers:
		if layer.isSpecialLayer and hasattr(layer, 'axes'):
			if layer.axes == axes:
				return layer
		else:
			match = True
			for i, axis in enumerate(axes):
				if axis != layer.master.axes[i]:
					match = False
					continue
			if match:
				return layer

def setMaster(font, tab, textCursor, textRange, toggle, newMasterIndex):
	# select the layers
	tab.textCursor = textCursor
	tab.textRange = textRange
	# set master index
	font.masterIndex = newMasterIndex+toggle
	font.masterIndex -= toggle

def setMasterLayersToMaster(tab, newMaster, currentMaster=None):
	# get user's selection
	currentTextCursor = tab.textCursor
	currentTextRange = tab.textRange
	font = newMaster.font
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


def toggleLayers(selectedLayers, master, tab):
	allNextLayers = getAllNextLayers(selectedLayers)
	# get layer indices
	selectionStart = tab.textCursor
	selectionEnd = tab.textCursor + tab.textRange
	selectedText = tab.layers[ selectionStart : selectionEnd ]

	tabLayers = []
	for i, layer in enumerate(tab.layers):
		if selectionStart <= i < selectionEnd or (selectionStart == selectionEnd and i == selectionStart):
			nextLayerAxes = allNextLayers[str(layer.axes)]
			nextLayer = getLayerForAxes(nextLayerAxes, layer)
			if nextLayer:
				tabLayers.append(nextLayer)
		else:
			tabLayers.append(layer)
	tab.layers = tabLayers

	# reset master layers to current font master
	setMasterLayersToMaster(tab, master)


def toggleAxis():
	font = Glyphs.font
	tab = font.currentTab
	selectedMaster = font.selectedFontMaster

	if not tab or not font.selectedLayers:
		toggleMaster( selectedMaster )
	
	else:
		# check if text tool is selected
		if Glyphs.currentDocument.windowController().toolDrawDelegate().className() in ['GlyphsToolText', 'GlyphsToolHand']:
			textTool = True
		else:
			textTool = False

		# text tool mode and no range is selected
		if textTool and tab.textRange == 0:
			toggleMaster( selectedMaster )

		# change selected layers only
		else:
			toggleLayers( font.selectedLayers, selectedMaster, tab )

toggleAxis()