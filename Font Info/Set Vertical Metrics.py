#MenuTitle: Set Vertical Metrics
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from vanilla import FloatingWindow, List, TextBox, EditText, Button, CheckBox, Slider
from AppKit import NSApp, NSBezierPath, NSRect, NSColor
import math
import traceback # print(traceback.format_exc())

__doc__="""
Set vertical metrics.
"""

# NOTES
# This version is based on Google guide: https://github.com/googlefonts/gf-docs/blob/main/VerticalMetrics/README.md

Glyphs.clearLog()

def nicely_round(value):
	if int(value) == value:
		return int(value)
	return round(value, 1)

def round_up_to_multiple(number, multiple):
    return multiple * math.ceil(number / multiple)

def remap(oValue, oMin, oMax, nMin, nMax):
	oRange = (oMax - oMin)
	if oRange == 0:
		nValue = nMin
	else:
		nRange = (nMax - nMin)  
		nValue = (((oValue - oMin) * nRange) / oRange) + nMin
	return nValue


GSSteppingTextField = objc.lookUpClass("GSSteppingTextField")
class ArrowEditText(EditText):
	nsTextFieldClass = GSSteppingTextField
	def _setCallback(self, callback):
		objc.super(ArrowEditText, self)._setCallback(callback)
		if callback is not None:
			self._nsObject.setContinuous_(True)
			self._nsObject.setAction_(self._target.action_)
			self._nsObject.setTarget_(self._target)

class SetVerticalMetrics():
	def __init__(self):
		self.close_previous_windows()

		self.font = Glyphs.font
		if not self.font:
			print('No font is open')
			return

		self.selected_masters = []
		self.all_highest, self.all_lowest = [], []
		self.ignore_non_exporting_glyphs = True
		self.round = 10 # round all metric values to multiple of this

		self.win_metrics = [None, None]
		self.typo_metrics = [None, None, None]
		self.hhea_metrics = [None, None, None]

		self.show_metrics = [] # checkboxes: 1 win 2 typo 3 hhea
		self.colors =  [(1, 0, 0, 1), # win = red
						(0, 0, 1, .1), # typo = blue
						(0, 1, 0, .1)] # hhea = green
		
		W, H = 400, 500
		M = 10
		column = W/4
		self.w = FloatingWindow((W, H), 
			minSize = (400, 255),
			maxSize = (400, 2000),
			title = 'Set Vertical Metrics — ' + self.font.familyName,
			autosaveName = 'com.slobzheninov.SetVerticalMetrics.mainwindow')
		
		# show checkboxes
		y = M
		self.w.show_title = TextBox((M, y, column, M*2), 'Show')
		self.w.show_win = CheckBox((column, y-1, column/2, M*2), 'Win', callback = self.show_callback)
		self.w.show_win.ID = 0
		self.w.show_typo = CheckBox((column*2, y-1, column/2, M*2), 'Typo', callback = self.show_callback)
		self.w.show_typo.ID = 1
		self.w.show_hhea = CheckBox((column*3, y-1, column/2, M*2), 'Hhea', callback = self.show_callback)
		self.w.show_hhea.ID = 2

		# metric titles
		mlt = 3
		ascender_y = y + M * mlt
		descender_y = ascender_y + M * mlt
		gap_y = descender_y + M * mlt

		self.w.ascender_title = TextBox((M, ascender_y, column, M*2), 'Ascender')
		self.w.descender_title = TextBox((M, descender_y, column, M*2), 'Descender')
		self.w.linegap_title = TextBox((M, gap_y, column, M*2), 'Line Gap')

		# ascender editors
		self.w.win_ascender = ArrowEditText((column, ascender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback)
		self.w.typo_ascender = ArrowEditText((column*2, ascender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback)
		self.w.hhea_ascender = ArrowEditText((column*3, ascender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback, placeholder = 'auto', )
		self.w.win_ascender.ID = 'win_ascender'
		self.w.typo_ascender.ID = 'typo_ascender'
		self.w.hhea_ascender.ID = 'hhea_ascender'

		# descender editors
		self.w.win_descender = ArrowEditText((column, descender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback)
		self.w.typo_descender = ArrowEditText((column*2, descender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback)
		self.w.hhea_descender = ArrowEditText((column*3, descender_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback, placeholder = 'auto', )
		self.w.win_descender.ID = 'win_descender'
		self.w.typo_descender.ID = 'typo_descender'
		self.w.hhea_descender.ID = 'hhea_descender'

		# line gap editors
		self.w.typo_linegap = ArrowEditText((column*2, gap_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback)
		self.w.hhea_linegap = ArrowEditText((column*3, gap_y, column-M, M*2), '', continuous = False, callback = self.metrics_callback, placeholder = 'auto')
		self.w.typo_linegap.ID = 'typo_linegap'
		self.w.hhea_linegap.ID = 'hhea_linegap'

		# line height and centering
		y = gap_y + M * mlt
		self.w.line_height_title = TextBox((M, y, column-M, M*2), 'Line Height')
		self.w.line_height = EditText((column, y, column/2.2, M*2), '', placeholder = '1.2')
		try:
			self.w.line_height.setToolTip('Defines the default line height, esp on the web.\nThe recommended value is about 1.2 because that’s the default in many apps')
		except:
			pass # Glyphs 2

		self.w.centering_title = TextBox((column*2, y, column-M, M*2), 'Center:  n')
		# self.w.centering = EditText((column*2.2, y, column/2.2, M*2), '1', placeholder = '0–1')
		self.w.centering_H = TextBox((-M*2.3, y, -M, M*2), 'H')
		self.w.centering = Slider((column*2.7, y, -M*3, M*2), value = 1, minValue = 0, maxValue = 1, tickMarkCount = 7, stopOnTickMarks = True, sizeStyle = 'mini')

		# checkboxes
		y = y + M * mlt
		self.w.use_typo = CheckBox((column*2, y, column*2, M*2), 'Use Typo Metrics (recommended)', sizeStyle = 'small', value = True)
		self.w.use_in_Glyphs = CheckBox((M+2, y, column*2, M*2), 'Use in Glyphs', sizeStyle = 'small', value = True)

		# masters table
		y = y + M * mlt
		self.w.masters = List((M, y, -M, -M*5),
				[{'Masters': master.name} for master in self.font.masters],
				columnDescriptions = [{'title': 'Masters', 'editable': False},
									{'title': 'Highest', 'editable': False},
									{'title': 'Lowest', 'editable': False}],
				doubleClickCallback = self.list_double_click,
				allowsSorting = False,
				allowsEmptySelection = False)
		self.w.masters.setSelection([i for i in range(len(self.font.masters))]) # select all by default

		# buttons
		self.w.calc = Button((M, -M*4, column-M*2, M*2), 'Calculate', callback = self.calc)	
		self.w.current = Button((column, -M*4, column-M*2, M*2), 'Current', callback = self.get_current)
		self.w.apply = Button((column*3, -M*4, column-M, M*2), 'Apply', callback = self.apply)
		
		self.add_callbacks()
		self.w.bind('close', self.remove_callbacks)
		self.w.open()

		self.get_current()
		

	def list_double_click(self, sender):
		if not sender.get():
			return

		new_layers = []
		for i in sender.getSelection():
			try:
				value = sender.get()[i]
				highest_glyph = self.font.glyphs[value['Highest'].split()[1]]
				highest_layer = highest_glyph.layers[self.font.masters[i].id]

				lowest_glyph = self.font.glyphs[value['Lowest'].split()[1]]
				lowest_layer = lowest_glyph.layers[self.font.masters[i].id]
				new_layers.extend([highest_layer, lowest_layer])
			except:
				print(traceback.format_exc())
		if new_layers:
			tab = self.font.currentTab if self.font.currentTab else self.font.newTab()
			new_tab_layers = list(tab.layers)
			# new_tab_layers.insert(tab.layersCursor, new_layers)
			new_tab_layers[tab.layersCursor:tab.layersCursor] = new_layers
			tab.layers = new_tab_layers


	def close_previous_windows(self):
		for window in NSApp.windows():
			if 'Set Vertical Metrics' in window.title():
				window.close()

	def add_callbacks(self):
		Glyphs.addCallback(self.draw_background, DRAWBACKGROUND)

	def remove_callbacks(self, sender):
		Glyphs.removeCallback(self.draw_background, DRAWBACKGROUND)

	def draw_background(self, current_layer, event):
		if not self.show_metrics:
			return

		for i in self.show_metrics:
			metric = [self.win_metrics, self.typo_metrics, self.hhea_metrics][i]
			
			if None in metric[:1]:
				continue

			self.rect(x = -100000,
						y = metric[1] if i != 0 else -metric[1],
						w = current_layer.width + 100000 * 2, 
						h = metric[0] - metric[1] if i != 0 else metric[0] + metric[1],
						color = self.colors[i],
						stroke = None if i != 0 else 5) # stroke for win, and fill for typo and hhea

	def rect(self, x, y, w, h, color, stroke = None):
		# make path
		rect = NSRect((x, y), (w, h))
		bezierPath = NSBezierPath.alloc().init()
		bezierPath.appendBezierPathWithRect_(rect)
		r, g, b, alpha = color
		NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, alpha).set()
		if stroke:
			bezierPath.setLineWidth_(stroke)
			bezierPath.stroke()
		else: # fill
			bezierPath.fill()

	def show_callback(self, sender):
		if sender.get():
			if sender.ID not in self.show_metrics:
				self.show_metrics.append(sender.ID)
		else:
			if sender.ID in self.show_metrics:
				self.show_metrics.remove(sender.ID)

	def metrics_callback(self, sender = None):
		# if no sender, call this callback for all the buttons
		if sender is None:
			for edittext in [self.w.win_ascender, self.w.win_descender, self.w.typo_ascender, self.w.typo_descender, self.w.typo_linegap, self.w.hhea_ascender, self.w.hhea_descender, self.w.hhea_linegap]:
				self.metrics_callback(edittext)
			return

		if sender.get() != '':
			try:
				value = int(sender.get())
			except:
				value = 'fail'
		else:
			value = None

		kind, metric = sender.ID.split('_')
		i = ['ascender', 'descender', 'linegap'].index(metric)
		
		if kind == 'win':
			if value == 'fail':
				sender.set(self.win_metrics[i])
			else:
				self.win_metrics[i] = value
		elif kind == 'typo':
			if value == 'fail':
				sender.set(self.typo_metrics[i])
			else:
				self.typo_metrics[i] = value
		elif kind == 'hhea':
			if value == 'fail':
				sender.set(self.hhea_metrics[i])
			else:
				self.hhea_metrics[i] = value

	def get_highest_and_lowest(self, font):
		all_highest, all_lowest = [], []
		for i, master in enumerate(font.masters):
			masterID = master.id
			glyphs_bottoms_and_tops = []
			for glyph in font.glyphs:
				if glyph.export or not self.ignore_non_exporting_glyphs:
					glyphs_bottoms_and_tops.append([glyph.name, glyph.layers[masterID].bounds.origin.y, glyph.layers[masterID].bounds.origin.y + glyph.layers[masterID].bounds.size.height])
			highest = sorted(glyphs_bottoms_and_tops, key=lambda x: -x[2])[0]	# ['Aring', 0.0, 899.0]
			lowest = sorted(glyphs_bottoms_and_tops, key=lambda x: x[1])[0] 	# ['at', -249.0, 749.0]
			highest = nicely_round(highest[2]), highest[0]
			lowest = nicely_round(lowest[1]), lowest[0]
			all_highest.append(highest)
			all_lowest.append(lowest)

			# set to UI
			self.w.masters[i] = {'Highest': str(highest[0]) + '  ' + highest[1],
								'Lowest': str(lowest[0]) + '  ' + lowest[1]}
		return all_highest, all_lowest

	def get_highest_and_lowest_for_masters(self, indexes):
		selected_highest, selected_lowest = [], []
		for i in indexes:
			selected_highest.append(self.all_highest[i])
			selected_lowest.append(self.all_lowest[i])
		sel_highest = sorted(selected_highest, key=lambda x: -x[0])[0]
		sel_lowest = sorted(selected_lowest, key=lambda x: x[0])[0]
		return sel_highest, sel_lowest

	def get_highest_Aacute(self, font, indexes):
		if 'Aacute' not in font.glyphs:
			return None, None
		glyph = font.glyphs['Aacute']
		tops = [[glyph.layers[font.masters[i].id].bounds.origin.y + glyph.layers[font.masters[i].id].bounds.size.height, i] for i in indexes]
		highest = sorted(tops, key=lambda x: -x[0])[0]
		return highest # this is [y, i]

	def calc(self, sender = None):
		if not self.font:
			print('Font not found: ' + self.w.getTitle())
			return
		# self.font = Glyphs.font
		# if not self.font:
		# 	return
		# self.w.title = 'Set Vertical Metrics — ' + self.font.familyName
		# get current selection if any

		current_selection = self.w.masters.getSelection()
		self.w.masters.set([{'Masters': master.name} for master in self.font.masters])
		self.w.masters.setSelection(current_selection if current_selection else [i for i in range(len(self.font.masters))]) # set last selection or all by default

		self.all_highest, self.all_lowest = self.get_highest_and_lowest(self.font)
		selected_masters_indexes = self.w.masters.getSelection()

		# get lowest and highest for the selection
		sel_highest, sel_lowest = self.get_highest_and_lowest_for_masters(selected_masters_indexes)

		# ----- set WIN
		# simply set to lowest and highest glyphs
		self.w.win_ascender.set(round_up_to_multiple(sel_highest[0], self.round))
		self.w.win_descender.set(round_up_to_multiple(abs(sel_lowest[0]), self.round)) # absolute
		
		# ----- set TYPO
		# The sum of the font’s vertical metric values (absolute) should be 20-30% greater than the font’s UPM: 
		# https://github.com/googlefonts/gf-docs/blob/main/VerticalMetrics/README.md#11-the-sum-of-the-fonts-vertical-metric-values-absolute-should-be-20-30-greater-than-the-fonts-upm
		# try:
		# 	centering = float(self.w.centering.get())
		# 	if not 0 < centering < 1:
		# 		to_except # this should skip to except
		# except:
		# 	centering = 1 # 0 = center to xHeight, 1 = center to capHeight
		# 	self.w.centering.set(centering)
		try:
			line_height = float(self.w.line_height.get())
		except:
			line_height = None


		# use Aacute (WIP: needs a fallback alternative)
		highest_Aacute, master_index = self.get_highest_Aacute(self.font, selected_masters_indexes)
		if highest_Aacute:
			master = self.font.masters[master_index]
			minimal_ascender = round_up_to_multiple(highest_Aacute, self.round)
			center = remap(self.w.centering.get(), 0, 1, master.xHeight/2, master.capHeight/2)
			dist = minimal_ascender - center
			minimal_descender = center - dist

			# ----- apply line height
			current_line_height_abs = minimal_ascender - minimal_descender
			current_line_height = round(current_line_height_abs / self.font.upm, 2)

			# no line_height input, use Aacute
			if line_height is None:
				self.w.line_height.set(str(current_line_height))

				ascender = minimal_ascender
				descender = minimal_descender

			# add leading to both ascender and descender
			else:
				diff = self.font.upm * line_height - current_line_height_abs
				diff = diff + 1 if diff % 2 != 0 else diff # make sure the difference is even
				ascender = round_up_to_multiple(minimal_ascender + diff/2, self.round)
				descender = -round_up_to_multiple(abs(minimal_descender - diff/2), self.round)

				# if shorter than Aacute, notify
				if current_line_height > line_height:
					Glyphs.showMacroWindow()
					print('Line height measured by Aacute is ', current_line_height, ', your input is shorter: ', line_height)

		self.w.typo_ascender.set(ascender)
		self.w.typo_descender.set(descender)
		self.w.typo_linegap.set('0')

		# ----- set HHEA to auto
		self.w.hhea_ascender.set('')
		self.w.hhea_descender.set('')
		self.w.hhea_linegap.set('')

		# run the callbacks for all the buttons
		self.metrics_callback()
		

	def get_current(self, sender = None):
		# self.font = Glyphs.font
		if not self.font:
			print('Font not found: ' + self.w.getTitle())
			return
		for parameter, textbox in {
				'typoAscender': 	self.w.typo_ascender,
				'typoDescender': 	self.w.typo_descender,
				'typoLineGap': 		self.w.typo_linegap,
				'hheaAscender':  	self.w.hhea_ascender,
				'hheaDescender': 	self.w.hhea_descender,
				'hheaLineGap': 		self.w.hhea_linegap,
				'winAscent': 		self.w.win_ascender,
				'winDescent': 		self.w.win_descender,
		}.items():
			value = self.font.selectedFontMaster.customParameters[parameter]
			textbox.set(value)
		# set line height if empty
		try:
			if not self.w.line_height.get():
				current_line_height_abs = self.w.typo_ascender.get() - self.w.typo_descender.get()
				self.w.line_height.set(round(current_line_height_abs / self.font.upm, 2))
		except:
			pass
		# run the callbacks for all the buttons
		self.metrics_callback()


	def apply(self, sender=None):
		# apply to the current font
		# self.font = Glyphs.font
		if not self.font:
			print('Font not found: ' + self.w.getTitle())
			return

		for value in self.win_metrics + self.typo_metrics:
			if value is None:
				print('The script expects all WIN and TYPO parameters to work')
				return

		selected_masters_indexes = self.w.masters.getSelection()
		for i in selected_masters_indexes:
			master = self.font.masters[i]

			master.customParameters['winAscent'] = self.win_metrics[0]
			master.customParameters['winDescent'] = self.win_metrics[1]

			master.customParameters['typoAscender'] = self.typo_metrics[0]
			master.customParameters['typoDescender'] = self.typo_metrics[1]
			master.customParameters['typoLineGap'] = self.typo_metrics[2]

			master.customParameters['hheaAscender'] = self.hhea_metrics[0] if self.hhea_metrics[0] is not None else self.typo_metrics[0]
			master.customParameters['hheaDescender'] = self.hhea_metrics[1] if self.hhea_metrics[1] is not None else self.typo_metrics[1]
			master.customParameters['hheaLineGap'] = self.hhea_metrics[2] if self.hhea_metrics[2] is not None else self.typo_metrics[2]

		# set use typo metrics
		self.font.customParameters['Use Typo Metrics'] = self.w.use_typo.get()

		# set custom parameter (use in Glyphs)
		if self.w.use_in_Glyphs.get():
			self.font.customParameters['EditView Line Height'] = self.typo_metrics[0] - self.typo_metrics[1] + self.typo_metrics[2]




SetVerticalMetrics()