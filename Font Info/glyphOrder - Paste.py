#MenuTitle: glyphOrder - Paste
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from Foundation import NSString, NSPasteboard, NSUTF8StringEncoding
__doc__="""
Pastes copied glyph names to selected index in glyphOrder.
1. Copy glyph names (space separated)
2. Select glyph, in front of which you want to paste them
3. Run this script
If glyphOrder custom parameter is missing, it will be created.
"""
Glyphs.clearLog()
font = Glyphs.font


def getGlyphNamesFromPasteboard():
	# get glyph names from pasteboard
	pasteboard = NSPasteboard.generalPasteboard()
	typeName = pasteboard.availableTypeFromArray_(["public.utf8-plain-text"])
	data = pasteboard.dataForType_(typeName)
	text = NSString.alloc().initWithData_encoding_(data, NSUTF8StringEncoding)
	copiedGlyphs = text.split()
	return copiedGlyphs

def filterCopiedGlyphs( copiedGlyphs ):
	glyphs = []
	for glyph in copiedGlyphs:
		if glyph in font.glyphs:
			glyphs.append( glyph )
	return glyphs

def getGlyphOrder():
	# create if missing
	if 'glyphOrder' not in font.customParameters:
		glyphOrder = []
		for glyph in font.glyphs:
			glyphOrder.append( glyph.name )
	else:
		glyphOrder = list( font.customParameters['glyphOrder'] )
	return glyphOrder

def removeFromGlyphsOrder( glyphOrder, copiedGlyphs ):
	for glyph in copiedGlyphs:
		if glyph in glyphOrder:
			glyphOrder.remove( glyph )
	return glyphOrder

def getSelectedIndex( glyphOrder ):
	if font.selectedLayers:
		selectedGlyph = font.selectedLayers[0].parent.name
		selectedIndex = glyphOrder.index( selectedGlyph )
		return selectedIndex

def pasteToIndex( copiedGlyphs, index, glyphOrder ):
	glyphOrder[ index:index ] = copiedGlyphs
	return glyphOrder

def setCustomParameter( glyphOrder ):
	font.customParameters['glyphOrder'] = glyphOrder

# run
copiedGlyphs = getGlyphNamesFromPasteboard()
copiedGlyphs = filterCopiedGlyphs( copiedGlyphs )
glyphOrder = getGlyphOrder()
glyphOrder = removeFromGlyphsOrder( glyphOrder, copiedGlyphs )
selectedIndex = getSelectedIndex( glyphOrder )
glyphOrder = pasteToIndex( copiedGlyphs, selectedIndex, glyphOrder )
setCustomParameter( glyphOrder )