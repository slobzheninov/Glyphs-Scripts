#MenuTitle: Previous Layer in Selection
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import traceback
from copy import copy

__doc__ = """
Switches to the previous layer in all selected glyphs in a tab.
Uses the first glyph’s layers to determine “next layer”.
"""

from GlyphsApp import Glyphs

direction = -1  # -1 = previous, 1 = next


def get_prev_or_next_layer(layer, direction):
	try:
		layers = layer.parent.sortedLayers()
		layer_index = layers.indexOfObject_(layer) + direction
		if layer_index < 0:
			layer_index = len(layers) - 1
		elif layer_index >= len(layers):
			layer_index = 0
		new_layer = layers[layer_index]
		return new_layer
	except:
		return None


def apply_layer_to_selected_glyphs(new_layer, selected_layers):
	new_selected_layers = []
	for layer in selected_layers:
		l = layer.parent.layerForName_(new_layer.name)
		new_selected_layers.append(l if l else layer)
	return new_selected_layers


def set_master(font, tab, text_cursor, text_range, toggle, master_index):
	# select the layers
	tab.textCursor = text_cursor
	tab.textRange = text_range
	# set master index
	font.masterIndex = master_index + toggle
	font.masterIndex -= toggle


def set_master_layers_to_master(font, tab, master):
	# get user's selection to reset later
	current_text_cursor = tab.textCursor
	current_text_range = tab.textRange
	master_index = font.masters.index(master)

	# toggle master to some other master and back, otherwise it doesn't apply
	toggle = -1 if 0 < master_index else 1

	# select old master layers and apply master
	text_cursor = None
	text_range = 0
	for i, layer in enumerate(tab.layers):
		if layer.isMasterLayer and layer.master == master:
			if text_cursor is None:
				text_cursor = i
			text_range += 1
		else:
			if text_cursor is not None:
				set_master(font, tab, text_cursor, text_range, toggle, master_index)
			# reset selection
			text_cursor = None
			text_range = 0
	if text_cursor is not None:
		set_master(font, tab, text_cursor, text_range, toggle, master_index)

	# set original user's selection
	tab.textCursor = current_text_cursor
	tab.textRange = current_text_range


def text_range_for_layers(layers):
    return sum(1 if layer.parent.unicode else 2 for layer in layers)


def switch_layers(direction=1):
	font = Glyphs.font
	if not font or not font.currentTab or not font.selectedLayers:
		return
	# get initial tab layers
	tab = font.currentTab
	initial_tab_layers = copy(tab.layers)

	# get text selection
	selection_start = tab.layersCursor
	selection_end = tab.layersCursor + len(tab.selectedLayers)
	first_layer = tab.layers[tab.layersCursor]

	try:
		new_first_layer = get_prev_or_next_layer(first_layer, direction)
	except:
		print(traceback.format_exc())
		return

	# apply the new layer to all selected glyphs; skip if not possible
	selected_layers = tab.selectedLayers
	new_selected_layers = apply_layer_to_selected_glyphs(new_first_layer, selected_layers)

	# apply layers to the whole tab or only selected layers
	if tab.textRange:
		new_tab_layers = initial_tab_layers[:selection_start] + new_selected_layers + initial_tab_layers[selection_end:]
	else:
		new_tab_layers = initial_tab_layers[:selection_start] + new_selected_layers + initial_tab_layers[selection_start + 1:]
	tab.layers = new_tab_layers

	set_master_layers_to_master(font, tab, font.masters[tab.masterIndex])


switch_layers(direction)