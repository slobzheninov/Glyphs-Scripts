#MenuTitle: Rotate
# -*- coding: utf-8 -*-
__doc__="""
Rotate
"""

import math

Font = Glyphs.font
selectedLayer = Font.selectedLayers[0]
selection = selectedLayer.selection

selectionXList = [n.x for n in selection]
selectionYList = [n.y for n in selection]
leftMostX, rightMostX = min(selectionXList), max(selectionXList)
lowestY, highestY = min(selectionYList), max(selectionYList)


def rotateLayer(thisLayer):
    # move on top of origin point:
    xCenter = (leftMostX+rightMostX)/2
    yCenter = (lowestY+highestY)/2
    shiftMatrix = [1, 0, 0, 1, -xCenter, -yCenter]
    thisLayer.applyTransform( shiftMatrix )

    # rotate around origin:
    angle = 10
    angleRadians = math.radians( angle )
    rotationMatrix = [ math.cos(angleRadians), -math.sin(angleRadians), math.sin(angleRadians), math.cos(angleRadians), 0, 0 ]
    thisLayer.applyTransform( rotationMatrix )

    # move back:
    shiftMatrix = [1, 0, 0, 1, xCenter, yCenter]
    thisLayer.applyTransform( shiftMatrix )

# loop through all selected layers:
selectedLayers = Glyphs.font.selectedLayers
for thisLayer in selectedLayers:
    rotateLayer(thisLayer)
