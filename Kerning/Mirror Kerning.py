#MenuTitle: Mirror Kerning
# -*- coding: utf-8 -*-
__doc__="""
Mirrors kerning for groups marked with | symbol. Save before using, sometimes crashes!
"""

thisFont = Glyphs.font # frontmost font
thisMaster = thisFont.selectedFontMaster # active master
thisMasterID = thisMaster.id # active master ID
thisKernDict = thisFont.kerning[thisMasterID] # kerning dictionary

tabText = "Not equal kerning:\n"
openNewTab = False
macroText = "Kerning mirrored:\n"
openMacro = False

 
# ------------------------------------ Collect mirroring groups ---------------------------

# Collects left mirroring groups
leftMirroringGroups = {}
subcat = {}

for glyph in thisFont.glyphs:
	if "|" in glyph.leftKerningKey:
		if glyph.leftKerningKey not in leftMirroringGroups:
			key = glyph.leftKerningKey
			
			if glyph.leftKerningKey.replace('@MMK_R_|', '') in thisFont.glyphs:
				value = glyph.leftKerningKey.replace('@MMK_R_|', '')
			else:			
				value = glyph.name
			leftMirroringGroups[key] = value 
			subcat[key] = glyph.subCategory #lowercase, uppercase, etc


# Collects right mirroring groups
rightMirroringGroups = {}
for glyph in thisFont.glyphs:
	if "|" in glyph.rightKerningKey:
		if glyph.rightKerningKey not in rightMirroringGroups:
			key = glyph.rightKerningKey
			
			if glyph.rightKerningKey.replace('@MMK_L_|', '') in thisFont.glyphs:
				value = glyph.rightKerningKey.replace('@MMK_L_|', '')
			else:			
				value = glyph.name
			rightMirroringGroups[key] = value 
			subcat[key] = glyph.subCategory #lowercase, uppercase, etc


# ------------------------------------ Go through kerning dict ---------------------------

 
for leftGlyphID in thisKernDict.keys():
	for rightGlyphID in thisKernDict[leftGlyphID].keys():
		if "|" in leftGlyphID and "|" in rightGlyphID: # mirroring group names should be marked with a bar symbol		
			
			leftGroup = leftGlyphID
			rightGroup = rightGlyphID
			
			kerningValue = thisFont.kerningForPair(thisMasterID, leftGroup, rightGroup)

			mirroredLeftGroup = rightGlyphID.replace('_R', '_L')
			mirroredRightGroup = leftGlyphID.replace('_L', '_R')
			
			#keep print simple
			shortLeft = leftGroup.replace('@MMK_L_|', '')
			shortRight = rightGroup.replace('@MMK_R_|', '')
			shortMirLeft = mirroredLeftGroup.replace('@MMK_L_|', '')
			shortMirRight = mirroredRightGroup.replace('@MMK_R_|', '')
			
			#letters belonging to groups
			glyphLeft = rightMirroringGroups[ leftGroup ]
			glyphRight = leftMirroringGroups[ rightGroup ]
			glyphMirLeft = rightMirroringGroups[ mirroredLeftGroup ]
			glyphMirRight = leftMirroringGroups[ mirroredRightGroup ]
			
			#check subcategories of the groups
			leftSubcat = subcat[ leftGroup ]
			rightSubcat = subcat[ rightGroup ]

			
			#ignore uppercase to lowercase mirroring
			if not ((leftSubcat == "Lowercase" and rightSubcat == "Uppercase") or (rightSubcat == "Lowercase" and leftSubcat == "Uppercase")):
			
			
				#kern if the mirrored pair doesn't exist
				if  thisFont.kerningForPair(thisMasterID, mirroredLeftGroup, mirroredRightGroup) > 1000000:
					thisFont.setKerningForPair(thisMasterID, mirroredLeftGroup, mirroredRightGroup, kerningValue) # !!! This seems to crash Glyphs sometimes!!!
					#print(shortMirLeft, kerningValue, shortMirRight, "was created")
					macroText += "@%s @%s: %s\n" % (shortMirLeft, shortMirRight, kerningValue)
					#print (macroText)
					openMacro = True
					
				# if the mirrored pair exists but is not equal open a new tab
				elif thisFont.kerningForPair(thisMasterID, mirroredLeftGroup, mirroredRightGroup) != thisFont.kerningForPair(thisMasterID, leftGroup, rightGroup): 
					#print (shortLeft, shortRight, "not equal to", shortMirLeft, shortMirRight)
					
					#test if mirrored pair is in tabText to avoid duplicating
					tabTest = "/%s/%s/%s" % (glyphRight, glyphLeft, glyphMirLeft)
					if tabTest not in tabText:
						if leftSubcat == "Uppercase":
							tabText += "HOH/%s/%s/%s HOH\n" % (glyphLeft, glyphRight, glyphMirRight)
						else:
							tabText += "nou/%s/%s/%s nou\n" % (glyphLeft, glyphRight, glyphMirRight)
						openNewTab = True


									
				# if mirrored kerning is equal, do nothing	
				#else:
				#	 print (shortLeft, shortRight, "equal to", shortMirLeft, shortMirRight)
				 



# ------------------------------------ Open a tab --------------------
if openMacro is True:
	Glyphs.showMacroWindow()
	print(macroText[:-1])

if openNewTab is True: 
	thisFont.newTab(tabText[:-1]) #check if the tab already exists


