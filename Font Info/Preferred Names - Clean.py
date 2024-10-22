#MenuTitle: Clean Preferred Names
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Deletes preferredFamilyName and preferredSubfamilyName custom parameters.
"""

from GlyphsApp import Glyphs

thisFont = Glyphs.font
cpName = ["preferredFamilyName", "preferredSubfamilyName"]

for thisInstance in thisFont.instances:
	if not thisInstance.active:
		continue

	#print("Processing Instance:", thisInstance.name)
	for j in range(len(cpName)):
		for i in reversed(range(len(thisInstance.customParameters))):
			if thisInstance.customParameters[i].name == cpName[j]:
				del thisInstance.customParameters[i]
				print("Deleted from:", thisInstance.name)
