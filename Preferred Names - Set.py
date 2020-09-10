#MenuTitle: Set Preferred Names
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Copies familyName to preferredFamilyName, instance name to preferredSubfamilyName.
Active instances only.
"""

thisFont = Glyphs.font # frontmost font


for thisInstance in thisFont.instances:

	if thisInstance.active:

		print("Processing Instance:", thisInstance.name)
		preferredFamilyName = thisFont.familyName

		if thisInstance.customParameters["preferredFamilyName"]:
			preferredFamilyName = thisInstance.customParameters["preferredFamilyName"]

		if thisInstance.customParameters["preferredSubfamilyName"]:
			preferredFamilyName = thisInstance.customParameters["preferredSubfamilyName"]

		thisInstance.customParameters["preferredFamilyName"] = preferredFamilyName
		thisInstance.customParameters["preferredSubfamilyName"] = thisInstance.name
		#print("   preferredFamilyName:", preferredFamilyName)
		#print("   preferredSubfamilyName:", preferredStyleName)


