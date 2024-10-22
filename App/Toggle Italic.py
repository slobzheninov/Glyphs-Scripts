#MenuTitle: Toggle Italic
# -*- coding: utf-8 -*-
__doc__ = """
Toggles along masters across the Italic or Slant axis.
"""

from ToggleAxis import toggleAxis
from GlyphsApp import Glyphs


def getItalicAxis():
	for i, axis in enumerate(Glyphs.font.axes):
		if Glyphs.versionNumber < 3:
			if axis['Tag'] == 'ital' or axis['Tag'] == 'slnt':
				return i
		else:
			if axis.axisTag == 'ital' or axis.axisTag == 'slnt':
				return i


toggleAxis(getItalicAxis())
