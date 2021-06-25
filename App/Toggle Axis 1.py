#MenuTitle: Toggle Axis 1
# -*- coding: utf-8 -*-
__doc__="""
Toggles along masters across the 1st axis in current tab.
"""
from Foundation import NSUserDefaults, NSString

font = Glyphs.font
tab = font.currentTab
selectedMaster = font.selectedFontMaster


theAxisIndex = 1 # toggle across axis number

theAxisIndex -= 1 # cuz in python we count from 0

try:
	def getTheAxisValue( master ):
	  return master.axes[ theAxisIndex ]


	# find "related" masters along the axis
	relatedMasters = []
	for master in font.masters:
		if master != selectedMaster:
			related = True
			for i, axis in enumerate( master.axes ):
				if i != theAxisIndex:
					if axis != selectedMaster.axes[ i ]:
						related = False
			if related is True:
				relatedMasters.append( master )

	# sort by italic value
	relatedMasters.sort( key = getTheAxisValue )

	# find next master
	toggleTo = None
	for master in relatedMasters:
		if master.axes[ theAxisIndex ] > selectedMaster.axes[ theAxisIndex ]:
			toggleTo = master
			break
	if not toggleTo:
		toggleTo = relatedMasters[0]

	# toggle master in current tab
	for i, master in enumerate(font.masters):
		if master == toggleTo:
			tab.masterIndex = i			
except:
	print('sorry, there is no axis %s' % theAxisIndex)
