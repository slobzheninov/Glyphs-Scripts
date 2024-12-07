#MenuTitle: Toggle Italic
# -*- coding: utf-8 -*-
__doc__ = """
Toggles along masters across the Italic or Slant axis.
"""

from ToggleAxis import toggleAxis
from GlyphsApp import Glyphs


def getItalicAxis():
	for i, axis in enumerate(Glyphs.font.axes):
		axisTag = axis['Tag'] if Glyphs.versionNumber < 3 else axis.axisTag
		if axisTag in ['ital', 'slnt']:
			axis = i
			return axis

toggleAxis(getItalicAxis())