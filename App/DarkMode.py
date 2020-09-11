#MenuTitle: Dark Mode
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Toggles dark mode preview.
"""

if Glyphs.defaults["GSEditViewDarkMode"] is True:
	Glyphs.defaults["GSEditViewDarkMode"] = False
else:
	Glyphs.defaults["GSEditViewDarkMode"] = True
