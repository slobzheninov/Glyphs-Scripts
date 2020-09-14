#MenuTitle: Text Simplifier
# -*- coding: utf-8 -*-
__doc__="""
Removes characters from a text. Useful for testing WIP fonts.
"""
import string
import vanilla
import re
from Foundation import NSUserDefaults, NSString

thisFont = Glyphs.font
openNewTab = False

m = 15 # margin
tm = 35 # top/vertical margin
bm = 50 # bottom margin
glyphBox = 100 #bottom text box

class TextSimplifier ( object ):
	
	def __init__(self):
		# Window 'self.w':
		windowWidth  = 200
		windowHeight = 360
		windowWidthResize  = 1200 # user can resize width by this value
		windowHeightResize = 500 # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Text Simplifier", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "save.TextSimplifier.mainwindow" # stores last window position and size
		)
		
		
		# UI elements:
			
		self.w.text_inpt = vanilla.TextBox( (m, m-3, m, tm), "Input:", sizeStyle='small' )
		self.w.text_outpt = vanilla.TextBox( (m, m, m, tm), "Output:", sizeStyle='small')
		self.w.text_glyphs = vanilla.TextBox( (m, m, m, tm), "Character set:", sizeStyle='small' )
		
		self.w.inpt = vanilla.TextEditor( (m, tm, m, tm), callback=self.SavePreferences, checksSpelling=False )
		self.w.outpt = vanilla.TextEditor( (m, tm, m, tm), callback=self.SavePreferences, checksSpelling=False, readOnly='True')
		self.w.glyphs = vanilla.TextEditor( (m, tm, m, tm), callback=self.SavePreferences, checksSpelling=False )

		self.windowResize(None)
		self.w.bind("resize",self.windowResize)
		
		# Run Button:
		self.w.runButton = vanilla.Button((-80-m, -20-m, -m, m), "Simplify", sizeStyle='regular', callback=self.TextSimplifier )
		self.w.setDefaultButton( self.w.runButton )
		
		# Reset Button:
		self.w.resetButton = vanilla.Button(((-80-m)*2, -20-m, (-80-m)-m, m), "Reset", sizeStyle='regular', callback=self.ResetParameters )
		
		# Open in a new Tab checkbox
		self.w.newTab = vanilla.CheckBox((m, -20-m, (-80-m)-m, m), "Open in a New Tab", sizeStyle='regular', value=False )

		
		
		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Text Simplifier' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
	

	def windowResize( self, sender ):
		windowWidth = self.w.getPosSize()[2]
		adaptiveWidth = windowWidth/2 - m*3/2
		
		
		self.w.text_inpt.setPosSize( (m, m-3, adaptiveWidth, tm) )
		self.w.text_outpt.setPosSize( (adaptiveWidth + m*2, m-3, adaptiveWidth, tm) )
		self.w.text_glyphs.setPosSize( (m, -glyphBox-bm-tm+m-3, -bm, -glyphBox) )
		
		self.w.inpt.setPosSize( (m, tm, adaptiveWidth, -glyphBox-bm-tm) )
		self.w.outpt.setPosSize( (adaptiveWidth + m*2, tm, adaptiveWidth, -glyphBox-bm-tm) )
		self.w.glyphs.setPosSize( (m, -glyphBox-bm, -m, glyphBox) )


		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["save.TextSimplifier.inpt"] = self.w.inpt.get()
			Glyphs.defaults["save.TextSimplifier.outpt"] = self.w.outpt.get()
			Glyphs.defaults["save.TextSimplifier.glyphs"] = self.w.glyphs.get()

		except:
			return False
			
		return True


	def LoadPreferences( self ):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"save.TextSimplifier.inpt": "",
					"save.TextSimplifier.outpt": "",
					"save.TextSimplifier.glyphs": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z . , space",

				}
			)
			self.w.inpt.set( Glyphs.defaults["save.TextSimplifier.inpt"] )
			self.w.outpt.set( Glyphs.defaults["save.TextSimplifier.outpt"] )
			self.w.glyphs.set( Glyphs.defaults["save.TextSimplifier.glyphs"] )

		except:
			return False
			
		return True
		
		
	def ResetParameters ( self, sender):
		del Glyphs.defaults["save.TextSimplifier.outpt"]
		del Glyphs.defaults["save.TextSimplifier.glyphs"]
		self.w.outpt.set( Glyphs.defaults["save.TextSimplifier.outpt"] )
		self.w.glyphs.set( Glyphs.defaults["save.TextSimplifier.glyphs"] )
		
		
	def TextSimplifier (self, sender):
		glyphs = self.w.glyphs.get()
		inpt = self.w.inpt.get()
		outpt = re.sub(r"[^%s]" % glyphs, "", inpt)
		
		#print("input", inpt)
		#print("output", outpt)
		self.w.outpt.set(outpt)
		if self.w.newTab.get() == 1:
			thisFont.newTab(outpt)		

TextSimplifier()





