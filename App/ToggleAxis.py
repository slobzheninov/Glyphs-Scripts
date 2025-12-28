# -*- coding: utf-8 -*-
__doc__ = """
Toggles along masters across the 1st axis.
"""

from GlyphsApp import Glyphs, GSControlLayer, GSFontMaster
from copy import copy


def getNextMaster(master, relatedLayers, AXIS):
	for layer in relatedLayers:
		if getAxisValue(layer, AXIS) > master.axes[AXIS]:
			return layer
	return relatedLayers[0]


def getRelatedMasters(selectedMaster, AXIS):
	# find "related" layers along the axis
	relatedMasters = []
	for master in selectedMaster.font.masters:
		if master != selectedMaster:
			related = True
			for i, axis in enumerate(master.axes):
				if i != AXIS:
					if axis != selectedMaster.axes[i]:
						related = False
			if related is True:
				relatedMasters.append(master)
	return relatedMasters


def toggleMaster(master, AXIS):
	relatedMasters = getRelatedMasters(master, AXIS)
	nextMaster = getNextMaster(master, relatedMasters)

	tab = master.font.currentTab
	if tab:
		setMasterLayersToMaster(tab, newMaster=nextMaster, currentMaster=master)
	else:
		master.font.masterIndex = master.font.masters.index(nextMaster)


def setMaster(font, tab, textCursor, textRange, toggle, newMasterIndex):
	# select the layers
	tab.textCursor = textCursor
	tab.textRange = textRange
	# set master index
	font.masterIndex = newMasterIndex + toggle
	font.masterIndex -= toggle


def setMasterLayersToMaster(tab, newMaster, currentMaster=None):
	# get user's selection to reset later
	currentTextCursor = tab.textCursor
	currentTextRange = tab.textRange
	newMasterIndex = newMaster.font.masters.index(newMaster)
	if currentMaster is None:
		currentMaster = newMaster
	# toggle master to some other master and back, otherwise it doesn't apply
	if newMaster == currentMaster:
		toggle = -1 if 0 < newMasterIndex else 1
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
				setMaster(newMaster.font, tab, textCursor, textRange, toggle, newMasterIndex)
			# reset selection
			textCursor = None
			textRange = 0
	if textCursor is not None:
		setMaster(newMaster.font, tab, textCursor, textRange, toggle, newMasterIndex)

	# set original user's selection
	tab.textCursor = currentTextCursor
	tab.textRange = currentTextRange


def getAxisValue(layer, axis):
	axes = layer.tempDataForKey_("axes")
	if axes is None:
		axes = getLayerAxes(layer)
	return axes[axis]


def getLayerAxes(layer):
	if isinstance(layer, GSFontMaster):
		return layer.axes
	layerAxes = []
	if Glyphs.versionNumber >= 3:
		coordinates = layer.attributes["coordinates"]
		if coordinates:
			axes = layer.axes()
			for axis in axes:
				coordinate = coordinates.get(axis.axisId, 0)
				layerAxes.append(coordinate)
	else:
		if '{' in layer.name:
			axesStr = layer.name.replace('{', '').replace('}', '').replace(",", " ").split()
			for axis in axesStr:
				layerAxes.append(float(axis))
	if not layerAxes:
		layerAxes = layer.master.axes
	# layer.setTempData_forKey_(layerAxes)
	layer.setTempData_forKey_(layerAxes, "axes")
	return layerAxes


def getRelatedLayers(specialLayer, AXIS):
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
		layerAxes = getLayerAxes(layer)

		# check if all axes match (except for the AXIS)
		related = True
		for i, axis in enumerate(layerAxes):
			if i != AXIS:
				if axis != getAxisValue(specialLayer, i):
					related = False

		# append related layers
		if related is True:
			relatedLayers.append(layer)

	# sort by the AXIS value
	relatedLayers.sort(key=lambda layer: getAxisValue(layer, AXIS))
	return relatedLayers


def getNextSpecialLayerName(specialLayer, AXIS):
	relatedLayers = getRelatedLayers(specialLayer, AXIS)

	# {} layers
	if relatedLayers:
		nextSpecialLayer = getNextMaster(specialLayer.master, relatedLayers, AXIS)
		return nextSpecialLayer.name

	# non {} layers
	else:
		return specialLayer.name


def getNextMasterId(font, masterId, AXIS):
	master = font.masters[masterId]
	relatedMasters = getRelatedMasters(master, AXIS)
	nextMaster = getNextMaster(master, relatedMasters, AXIS)
	return nextMaster.id


def toggleMasterInTab(master, tab, AXIS):
	# get next master for current master and save it
	# go through each layer and if it’s different from master, find its next layer id, and save it too and swap.
	# in the line above also check in the list instead of finding again.

	cachedNextLayers = {}
	tempTabLayers = copy(tab.layers)

	# get next master to the tab master
	nextMasterId = getNextMasterId(master.font, master.id, AXIS)
	nextMaster = master.font.masters[nextMasterId]

	# cache next master and toggle tab master
	cachedNextLayers[master.id] = nextMasterId
	master.font.masterIndex = master.font.masters.index(nextMaster)

	# get layer selection
	selectionStart = tab.layersCursor
	selectionEnd = tab.layersCursor + len(tab.selectedLayers)

	# find layers different from tab master (check in the original/temp list)
	for i, layer in enumerate(tempTabLayers):

		# layer not selected (if any selection)
		if not (
			tab.textRange == 0
			or selectionStart <= i < selectionEnd
			or (selectionStart == selectionEnd and i == selectionStart)
		):
			continue

		# other master layer
		elif layer.isMasterLayer and layer.layerId != master.id:
			# get next layer (either from cache or do cache it)
			nextLayerId = cachedNextLayers.get(layer.layerId)
			if nextLayerId is None:
				nextLayerId = getNextMasterId(master.font, layer.layerId, AXIS)
				cachedNextLayers[layer.layerId] = nextLayerId
			nextLayer = layer.parent.layers[nextLayerId]
			tempTabLayers[i] = nextLayer

		# special layer
		elif layer.isSpecialLayer:
			nextLayerName = cachedNextLayers.get(layer.name)
			if nextLayerName is None:
				nextLayerName = getNextSpecialLayerName(layer, AXIS)
				cachedNextLayers[layer.name] = nextLayerName
			nextLayer = layer.parent.layers[nextLayerName]
			tempTabLayers[i] = nextLayer

		# control layer, skip
		elif isinstance(layer, GSControlLayer):
			continue

		# current master layer, just append
		else:
			tempTabLayers[i] = layer.parent.layers[nextMasterId]

	# apply new layers only if any differ from tab master OR if any selection
	if len(cachedNextLayers) > 1 or 0 < tab.textRange < len(tab.layers):
		tab.layers = tempTabLayers
		setMasterLayersToMaster(tab, nextMaster)


def toggleAxis(AXIS):
	font = Glyphs.font
	tab = font.currentTab
	selectedMaster = font.selectedFontMaster

	if AXIS is None or AXIS >= len(font.axes):
		print("Axis %s not found" % AXIS)
		return

	if not tab:
		toggleMaster(selectedMaster, AXIS)

	else:
		# get viewport position
		viewPort = tab.viewPort

		# toggle layers and masters
		toggleMasterInTab(selectedMaster, tab, AXIS)

		# restore viewport position
		tab.viewPort = viewPort
