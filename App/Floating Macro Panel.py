#MenuTitle: Floating Macro Panel
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Toggles Macro panel floating.
"""

from AppKit import NSApp, NSFloatingWindowLevel, NSNormalWindowLevel
from GlyphsApp import Glyphs

Glyphs.showMacroWindow()
for window in NSApp.windows():
	if window.className() == 'GSMacroWindow':
		# make normal
		if window.level() == 3:
			window.setLevel_(NSNormalWindowLevel)
			print('Macro panel is not floating now')
		# make floating
		else:
			window.setLevel_(NSFloatingWindowLevel)
			print('Macro panel is floating now')
		break
