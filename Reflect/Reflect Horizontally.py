#MenuTitle: Reflect Horizontally
# -*- coding: utf-8 -*-
__doc__="""
Reflect Horizontally.
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
	
	selectionXList = [ n.x for n in selection ]
	leftMostX, rightMostX = min( selectionXList ), max( selectionXList )
	diffX = abs(rightMostX-leftMostX)
	midX = rightMostX - diffX/2
	
	Font.disableUpdateInterface()

	sortedSelection = sorted( selection, key=lambda n: n.x)
	for thisNodeIndex in range( len(selection)):
		sortedSelection[thisNodeIndex].x = sortedSelection[thisNodeIndex].x-(sortedSelection[thisNodeIndex].x-midX)*2
			
	Font.enableUpdateInterface()
	
except Exception, e:
	if selection == ():
		print "Cannot align nodes: nothing selected in frontmost layer."
	else:
		print "Error. Cannot align nodes:", selection
		print e

