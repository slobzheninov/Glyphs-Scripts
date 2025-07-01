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
		'incompatiblity': 0,
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
		elements[layer.layerId]['name'] = layer.name
		
		flattened_layer = layer.copy()
		flattened_layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
		flattened_elements[layer.layerId] = count_layer_elements(flattened_layer)
		flattened_elements[layer.layerId]['name'] = layer.name

		no_overlaps_layer = layer.copy()
		no_overlaps_layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(True, None, None, None, None)
		no_overlaps_elements[layer.layerId] = count_layer_elements(no_overlaps_layer)
		no_overlaps_elements[layer.layerId]['name'] = layer.name
	return remove_unused_elements(elements), remove_unused_elements(flattened_elements), remove_unused_elements(no_overlaps_elements)


def get_layers_per_element(elements):
	layers_per_element = {}
	for layerId, layer_elements in elements.items():
		for element, count in layer_elements.items():
			if element not in layers_per_element:
				layers_per_element[element] = {}
			if count not in layers_per_element[element]:
				layers_per_element[element][count] = []
			layers_per_element[element][count].append(layerId)
	return layers_per_element


def get_imcompatibility_points(elements, layers_per_element):
	for element, count_dict in layers_per_element.items():
		if element == 'name':
			continue
		if len(count_dict) > 1:
			count_dict_sorted = sorted(count_dict.items(), key=lambda x: len(x[1]), reverse=True)

			# count main groups (groups with largest number of matches)
			main_groups_count = 0
			main_group_size = len(count_dict_sorted[0][1])
			for i in range(len(count_dict_sorted)):
				if len(count_dict_sorted[i][1]) == main_group_size:
					main_groups_count += 1
				else:
					break
			# add incompatiblity points to all groups whose element count differs from the main group
			for count, layerIds in count_dict_sorted[main_groups_count:]:
				for layerId in layerIds:
					elements[layerId]['incompatiblity'] += 1


def print_report(elements, glyph_name, level = 0, note = ''):
	indent = '   ' * level
	
	if note:
		print(f'{indent}{note}\n')
	else:
		print(f'{indent}--------------------  {glyph_name}  --------------------\n')
	
	for layerId, e in elements.items():
		if e['incompatiblity'] == 0:
			s = f'{indent}🟢 '
		elif e['incompatiblity'] < 3:
			s = f'{indent}🟡 '
		elif e['incompatiblity'] < 5:
			s = f'{indent}🟠 '
		else:
			s = f'{indent}🔴 '

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


	
def report_glyph_compatibility(glyph):
	elements, flattened_elements, no_overlaps_elements = get_elements_per_layer(glyph)

	layers_per_element = get_layers_per_element(elements)
	get_imcompatibility_points(elements, layers_per_element)

	flattened_layers_per_element = get_layers_per_element(flattened_elements)
	get_imcompatibility_points(flattened_elements, flattened_layers_per_element)

	no_overlaps_layers_per_element = get_layers_per_element(no_overlaps_elements)
	get_imcompatibility_points(no_overlaps_elements, no_overlaps_layers_per_element)

	print('* * *   Compatibility Report   * * *\n')
	print_report(elements, glyph.name)
	print_report(flattened_elements, glyph.name, level = 1, note = 'Flatten Outlines (variable export). Flattens masks, corner and cap components, sometimes regular components')
	print_report(no_overlaps_elements, glyph.name, level = 2, note = 'Flatten Outlines + Remove Overlaps (variable export with a “RemoveOverlap” filter)')
	print('\n')

	

for layer in set(Glyphs.font.selectedLayers):
	report_glyph_compatibility(layer.parent)


