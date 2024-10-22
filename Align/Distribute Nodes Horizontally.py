#MenuTitle: Distribute Nodes Horizontally
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Distributes the selected nodes horizontally.
"""

from GlyphsApp import Glyphs

# This is a slightly modified vertion of Distribute Nodes script by @mekkablue


def distributeNodes(direction):  # 0 horizontal, 1 vertical
	font = Glyphs.font
	if not font.selectedLayers:
		return
	selectedLayer = font.selectedLayers[0]
	try:
		try:
			# until v2.1:
			selection = selectedLayer.selection()
		except:
			# since v2.2:
			selection = selectedLayer.selection
		# nothing to distribute
		if len(selection) < 3:
			return

		selectionXList = [n.x for n in selection]
		selectionYList = [n.y for n in selection]
		leftMostX, rightMostX = min(selectionXList), max(selectionXList)
		lowestY, highestY = min(selectionYList), max(selectionYList)
		diffX = abs(leftMostX - rightMostX)
		diffY = abs(lowestY - highestY)

		font.disableUpdateInterface()
		try:
			if direction == 0:  # distribute horizontally
				increment = diffX / float(len(selection) - 1)
				sortedSelection = sorted(selection, key=lambda n: n.x)
				for thisNodeIndex in range(len(selection) - 1):
					sortedSelection[thisNodeIndex].x = leftMostX + (thisNodeIndex * increment)
			else:  # distribute vertically
				increment = diffY / float(len(selection) - 1)
				sortedSelection = sorted(selection, key=lambda n: n.y)
				for thisNodeIndex in range(len(selection) - 1):
					sortedSelection[thisNodeIndex].y = lowestY + (thisNodeIndex * increment)
		except Exception as e:
			Glyphs.showMacroWindow()
			print("\n⚠️ Script Error:\n")
			import traceback
			print(traceback.format_exc())
			print()
			raise e
		finally:
			font.enableUpdateInterface()  # re-enables UI updates in font View

	except Exception as e:
		if selection == ():
			print("Cannot distribute nodes: nothing selected in frontmost layer.")
		else:
			print("Error. Cannot distribute nodes:", selection)
			print(e)


distributeNodes(direction=0)
