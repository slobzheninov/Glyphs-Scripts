#MenuTitle: Toggle Italic
# -*- coding: utf-8 -*-
__doc__="""
Toggles between upright and italic masters in current tab.
"""
from Foundation import NSUserDefaults, NSString


# toggle between upright and italic masters in current tab
font = Glyphs.font
tab = font.currentTab
selectedMaster = font.selectedFontMaster


italicAxisIndex = None
for i, axis in enumerate( font.axes ):
	if axis['Tag'] == 'ital' or axis['Tag'] == 'slnt':
		italicAxisIndex = i
		break

def getItalicValue( master ):
  return master.axes[ italicAxisIndex ]


# find "related" masters along italic axis
relatedMasters = []
for master in font.masters:
	if master != selectedMaster:
		related = True
		for i, axis in enumerate( master.axes ):
			if i != italicAxisIndex:
				if axis != selectedMaster.axes[ i ]:
					related = False
		if related is True:
			relatedMasters.append( master )

# sort by italic value
relatedMasters.sort( key = getItalicValue )

# find next master
toggleTo = None
for master in relatedMasters:
	if master.axes[ italicAxisIndex ] > selectedMaster.axes[ italicAxisIndex ]:
		toggleTo = master
		break
if not toggleTo:
	toggleTo = relatedMasters[0]

# toggle master in current tab
for i, master in enumerate(font.masters):
	if master == toggleTo:
		tab.masterIndex = i			
