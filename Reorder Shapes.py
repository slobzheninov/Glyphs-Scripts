#MenuTitle: Reorder Shapes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Reorders paths by their length, y and x. Reorders components by glyph name, y and x.
"""
# sort paths by length, y, x
# sort components by glyph name, y, x
# round coordinates to 10, since anything smaller is probably an error

for selectedLayer in Font.selectedLayers:
	glyph = selectedLayer.parent
	for layer in glyph.layers:

		# glyphs 2
		if Glyphs.versionNumber < 3:
			layer.paths = sorted( layer.paths, key=lambda path: (len(path), round(path.bounds.origin.y, -1), round(path.bounds.origin.x, -1) ))
			layer.components = sorted( layer.components, key=lambda component: (component.name, round(component.bounds.origin.y, -1), round(component.bounds.origin.x, -1) ))
		
		# glyphs 3+
		else:
			# sort components
			components = sorted( layer.components, key=lambda component: (component.glyph.name, round(component.bounds.origin.y, -1), round(component.bounds.origin.x, -1) ))			
			for i, component in enumerate(reversed(components)):
				index = layer.shapes.index( component )
				layer.shapes.pop( index )
				layer.shapes.insert( 0, component )

			# sort paths
			paths = sorted( layer.paths, key=lambda path: (len(path), round(path.bounds.origin.y, -1), round(path.bounds.origin.x, -1) ))
			for i, path in enumerate(reversed(paths)):
				index = layer.shapes.index( path )
				layer.shapes.pop( index )
				layer.shapes.insert( 0, path )