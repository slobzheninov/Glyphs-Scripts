#MenuTitle: Mirror Kerning
# -*- coding: utf-8 -*-
__doc__="""
Mirrors kerning for groups marked with | symbol
"""

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
thisFontMasterID = thisFontMaster.id # active master ID
thisFontMasterKernDict = thisFont.kerning[thisFontMasterID] # kerning dictionary


def nameForID(Font, ID):
	if ID[0] == "@": # is a group
		return ID
	else: # is a glyph
		return Font.glyphForId_(ID).name


for leftGlyphID in thisFontMasterKernDict.keys():
	for rightGlyphID in thisFontMasterKernDict[ leftGlyphID ].keys():
		leftName  = nameForID( thisFont, leftGlyphID )
		rightName = nameForID( thisFont, rightGlyphID )	
		kerningValue = thisFont.kerningForPair(thisFont.selectedFontMaster.id, leftName, rightName)


		# mirrored left and right groups should be marked with | symbol: @|A or @|V, etc
		if "|" in leftName and "|" in rightName:
			
			# swap left and right groups
			left = rightName.replace('_R', '_L')
			right = leftName.replace('_L', '_R')
			

			# to keep print cleaner
			shortLeft = left.replace('@MMK_L_|', '') 
			shortRight = right.replace('@MMK_R_|', '')
			shortLeftName = leftName.replace('@MMK_L_|', '') 
			shortRightName = rightName.replace('@MMK_R_|', '')
			

			# create the mirrored pair if it doesn’t exist
			if  thisFont.kerningForPair(thisFont.selectedFontMaster.id, left, right) > 100000:
				thisFont.setKerningForPair(thisFont.selectedFontMaster.id, left, right, kerningValue)
				print(left, right, kerningValue, "was created")
				#print(shortLeft, shortRight, kerningValue, "was created")
				
		
			# if the mirrored pair exists but is not equal (open a new tab?)
			elif thisFont.kerningForPair(thisFont.selectedFontMaster.id, left, right) != thisFont.kerningForPair(thisFont.selectedFontMaster.id, leftName, rightName): 
				print (shortLeftName, shortRightName, "not equal to", shortLeft, shortRight)
				
				
			# if mirrored kerning is equal, do nothing	
			else:
				 print (shortLeftName, shortRightName, "equal to", shortLeft, shortRight)
				 
				 

		
