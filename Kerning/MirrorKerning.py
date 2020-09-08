#MenuTitle: Mirror Kerning (WIP)
# -*- coding: utf-8 -*-
__doc__="""
Mirrors kerning for groups marked with | symbol
"""

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
thisFontMasterID = thisFontMaster.id # active master ID
thisFontMasterKernDict = thisFont.kerning[thisFontMasterID] # kerning dictionary



for leftGlyphID in thisFontMasterKernDict.keys():
	for rightGlyphID in thisFontMasterKernDict[leftGlyphID].keys():
		if "|" in leftGlyphID and "|" in rightGlyphID: # mirroring group names should be marked with a bar symbol
			
			leftGroup = leftGlyphID
			rightGroup = rightGlyphID
			
			kerningValue = thisFont.kerningForPair(thisFont.selectedFontMaster.id, leftGroup, rightGroup)

			mirroredLeftGroup = rightGlyphID.replace('_R', '_L')
			mirroredRightGroup = leftGlyphID.replace('_L', '_R')
			

			#keep print simple
			shortLeft = leftGroup.replace('@MMK_L_|', '')
			shortRight = rightGroup.replace('@MMK_R_|', '')
			shortMirLeft = mirroredLeftGroup.replace('@MMK_L_|', '')
			shortMirRight = mirroredRightGroup.replace('@MMK_R_|', '')
			
			
			#if the mirrored pair doesn't exist
			if  thisFont.kerningForPair(thisFont.selectedFontMaster.id, mirroredLeftGroup, mirroredRightGroup) > 1000000:

				thisFont.setKerningForPair(thisFont.selectedFontMaster.id, mirroredLeftGroup, mirroredRightGroup, kerningValue) # this seem to crash Glyphs!
				print(shortMirLeft, kerningValue, shortMirRight, "was created")
				
				
			# if the mirrored pair exists but is not equal (open a new tab?)
			elif thisFont.kerningForPair(thisFont.selectedFontMaster.id, mirroredLeftGroup, mirroredRightGroup) != thisFont.kerningForPair(thisFont.selectedFontMaster.id, leftGroup, rightGroup): 
				print (shortLeft, shortRight, "not equal to", shortMirLeft, shortMirRight)
				
				
			# if mirrored kerning is equal, do nothing	
			else:
				 print (shortLeft, shortRight, "equal to", shortMirLeft, shortMirRight)
