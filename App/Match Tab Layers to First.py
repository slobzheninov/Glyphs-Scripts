#MenuTitle: Match Tab Layers to First
# -*- coding: utf-8 -*-
__doc__="""
Sets all tab layers to the first, wherever possible.
Useful for setting special layers.
"""
# from Foundation import NSUserDefaults, NSString
import re

font = Glyphs.font

def get_layer_axes_values(layer):
	if '{' in layer.name and '}' in layer.name:
		# Special layer
		return [float(axis_value) for axis_value in re.findall(r'{(.+)}', layer.name)[0].split(',')]
	else:
		# Non-special layer
		return [axis for axis in layer.master.axes]

def match_tab_layers_to_first():
	tab = font.currentTab
	if not tab:
		return

	# get the fist layer and its axes
	first_layer = tab.layers[0]
	first_layer_axes = get_layer_axes_values(first_layer)

	new_tab_layers = [first_layer]

	# for each glyph in the tab, find a layer with matching axes
	for layer in tab.layers[1:]:
		found = False
		for l in layer.parent.layers:
			l_axes = get_layer_axes_values(l)
			if l_axes == first_layer_axes:
				found = True
				break
		# add layer with the same axes
		if found:
			new_tab_layers.append(l)
		# no match, add the layer itself
		else:
			new_tab_layers.append(layer)

	# set new tab layers
	tab.layers = new_tab_layers


match_tab_layers_to_first()
