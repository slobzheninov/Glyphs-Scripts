#MenuTitle: Reflect Vertically
# -*- coding: utf-8 -*-
__doc__="""
Reflect Vertically.
"""



Font = Glyphs.font
Doc = Glyphs.currentDocument
selectedLayer = Font.selectedLayers[0]

try:
	try:
		# until v2.1:
		selection = selectedLayer.selection()
	except:
		# since v2.2:
		selection = selectedLayer.selection
	
	selectionYList = [ n.y for n in selection ]
	lowestY, highestY = min( selectionYList ), max( selectionYList )
	diffY = abs(lowestY-highestY)
	midY = highestY - diffY/2
	
	Font.disableUpdateInterface()

	sortedSelection = sorted( selection, key=lambda n: n.y)
	for thisNodeIndex in range( len(selection)):
		sortedSelection[thisNodeIndex].y = sortedSelection[thisNodeIndex].y-(sortedSelection[thisNodeIndex].y-midY)*2
			
	Font.enableUpdateInterface()
	
except Exception, e:
	if selection == ():
		print "Cannot align nodes: nothing selected in frontmost layer."
	else:
		print "Error. Cannot align nodes:", selection
		print e

