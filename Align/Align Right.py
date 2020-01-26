#MenuTitle: Align Right
# -*- coding: utf-8 -*-
__doc__="""
Align Left.
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
	
	Font.disableUpdateInterface()

	sortedSelection = sorted( selection, key=lambda n: n.x)
	for thisNodeIndex in range( len(selection)):
		sortedSelection[thisNodeIndex].x = rightMostX
			
	Font.enableUpdateInterface()
	
except Exception, e:
	if selection == ():
		print "Cannot align nodes: nothing selected in frontmost layer."
	else:
		print "Error. Cannot align nodes:", selection
		print e
