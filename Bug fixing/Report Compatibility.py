#MenuTitle: Report Compatibility
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""
Reports compatibility of the selected glyphs.
Separately reports compatibility for:
- Flatten outlines (which you get on variable export)
- Remove overlaps (variable export with the “remove overlaps” filter)
"""

Glyphs.clearLog()
Glyphs.showMacroWindow()
ELEMENTS = 'nodes, lines, curves, offcurves, paths, components, corner components, cap components, anchors, name'.split(', ')

def count_layer_elements(layer):
	nodes = [node for path in layer.paths for node in path.nodes]
	return {
		'paths': len(layer.paths),
		'nodes': len(nodes),
		'lines': len([node for node in nodes if node.type == LINE]),
		'curves': len([node for node in nodes if node.type == CURVE]),
		'offcurves': len([node for node in nodes if node.type == OFFCURVE]),
		'components': len(layer.components),
		'corner components': len([hint for hint in layer.hints if hint.type == CORNER]),
		'cap components': len([hint for hint in layer.hints if hint.type == CAP]),
		'anchors': len(layer.anchors),
		'name': layer.name,
	}


def remove_unused_elements(elements):
	for element in ELEMENTS:
		# check if element is used
		used = False
		for layerId, layer_elements in elements.items():
			if layer_elements[element] != 0:
				used = True
				continue
		# remove unused elements
		if used is False:
			for layerId, layer_elements in elements.items():
				del(layer_elements[element])
	return elements


def get_elements_per_layer(glyph):
	elements = {}
	flattened_elements = {}
	no_overlaps_elements = {}
	for layer in glyph.layers:
		elements[layer.layerId] = count_layer_elements(layer)
	return remove_unused_elements(elements)


def get_compatibility_groups(glyph):
	groups = {}
	for layer in glyph.layers:
		if layer.compareString() not in groups:
			groups[layer.compareString()] = []
		groups[layer.compareString()].append(layer)
	sorted_groups = dict(sorted(groups.items(), key=lambda item: len(item[1]), reverse=True))
	return sorted_groups

def get_group_colors(glyph, groups):
	COLORS = ['🟢🟡🟠🔴', '🟩🟨🟧🟥', '💚💛🧡❤️'] # ['🟢🟡🟠🔴🟣🔵⚫', '🟩🟨🟧🟥🟪🟦⬛', '💚💛🧡❤️💜💙🖤']
	group_colors = {}

	tier = -1
	max_tier = len(glyph.layers) - 1
	last_tier = None
	last_layer_count = None
	style = 0

	for compareString, layers in groups.items():
		current_layer_count = len(layers)

		if current_layer_count != last_layer_count:
			last_layer_count = current_layer_count
			tier = min(tier + 1, max_tier)
		
		if tier == last_tier:
			style += 1
			style = style % len(COLORS)
		else:
			style = 0

		last_tier = tier

		group_colors[compareString] = COLORS[style][tier]

	return group_colors
		

def print_report(glyph, elements, group_colors, level = 0, note = ''):
	indent = '   ' * level

	if note:
		print(f'{indent}{note}\n')
	else:
		print(f'{indent}--------------------  {glyph.name}  --------------------\n')
	
	for layerId, e in elements.items():

		s = f"{indent}{group_colors[glyph.layers[layerId].compareString()]} " 

		for element in ELEMENTS:
			if element in e:
				count = e[element]
				if element == 'name':
					s = s[:-2] + f" - {count}" # 'count' is the name
				else:
					if int(count) < 10: # add a space for single digits for a better alignment
						count = f" {count}"
					s += f"{count} {element}, "
		print(s)
	print('')


def report_glyph_compatibility(glyph, level = 0, note = ''):
	elements = get_elements_per_layer(glyph)
	groups = get_compatibility_groups(glyph)
	group_colors = get_group_colors(glyph, groups)
	print_report(glyph, elements, group_colors, level, note)
	

for layer in set(Glyphs.font.selectedLayers):
	glyph = layer.parent
	report_glyph_compatibility(glyph, level = 0)

	# flatten outlines
	flatten_glyph = GSGlyph()
	for i, l in enumerate(glyph.layers):
		flatten_layer = l.copy()
		flatten_layer.name = l.name
		flatten_layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
		flatten_glyph.layers.append(flatten_layer)
	report_glyph_compatibility(flatten_glyph, level = 1, note = 'Flatten Outlines (variable export). Flattens masks, corner and cap components, sometimes regular components')

	# flatten outlines
	remove_overlaps_glyph = GSGlyph()
	for i, l in enumerate(glyph.layers):
		remove_overlaps_layer = l.copy()
		remove_overlaps_layer.name = l.name
		remove_overlaps_layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(True, None, None, None, None)
		remove_overlaps_glyph.layers.append(remove_overlaps_layer)
	report_glyph_compatibility(remove_overlaps_glyph, level = 2, note = 'Flatten Outlines + Remove Overlaps (variable export with a “RemoveOverlap” filter)')



