#MenuTitle: Set Preferred Names
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Copies familyName to preferredFamilyName, instance name to preferredSubfamilyName.
Active instances only.
"""

from GlyphsApp import Glyphs

font = Glyphs.font


for thisInstance in font.instances:

	if not thisInstance.active:
		continue

	print("Processing Instance:", thisInstance.name)
	preferredFamilyName = font.familyName

	if thisInstance.customParameters["preferredFamilyName"]:
		preferredFamilyName = thisInstance.customParameters["preferredFamilyName"]

	if thisInstance.customParameters["preferredSubfamilyName"]:
		preferredFamilyName = thisInstance.customParameters["preferredSubfamilyName"]

	thisInstance.customParameters["preferredFamilyName"] = preferredFamilyName
	thisInstance.customParameters["preferredSubfamilyName"] = thisInstance.name
	#print("   preferredFamilyName:", preferredFamilyName)
	#print("   preferredSubfamilyName:", preferredStyleName)
