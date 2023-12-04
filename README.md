# About

These are scripts for [Glyphs](https://glyphsapp.com/). Some may not work in Glyphs 3, WIP.
Some scripts use Vanilla.

## Installation: 
Put the scripts into Scripts folder: Library – Application Support - Glyphs - Scripts
(Cmd + Shift + Y) or through Plugin Manager in Glyphs 3.

## Align, Reflect and Rotate
Align and reflect nodes and handles. Useful with keyboard shortcuts — I personally use Ctrl + Cmd + Arrow keys. Set it in System Preferences – Keyboard – Shortcuts.

### Align scripts features:
* align selected nodes;
* align paths (select the whole path) and components;
* align node to the next / previous node (select one node only);
* align to the next closest measurment line (vertical metrics, half x-height, half cap-height);
* takes into account the italic angle (which is super duper cool!);
* takes into account smooth connection (“green” nodes)
* NEW: with Caps Lock on, you can now align the whole selection to glyph metrics / measurment lines (vertical metrics, half x-height, half cap-height)

Center Selected Glyphs sets equal left and right sidebearings within the same width for all layers of selected glyphs.

## Export to All Formats
Batch-exports the currently active font to otf, ttf and web formats (woff, woff2). Optionally, exports each format to a subfolder. Optionally, exports all fonts currently open in Glyphs. Ignores variable exports.

## Preferred Names
Sets (or cleans) *preferredFamily* and *preferredSubfamily* instance custom parameters. Based on *Font Family Name* and *Instance / Style Name*. Useful for office apps compatibility.

## glyphOrder - Paste
A simple way to reorder glyphs with glyphOrder custom parameter.
1. Copy space separeted glyph names.
2. Select glyph, in front of which you want to paste them.
3. Run the script.
If glyphOrder custom parameter is missing, it will be created.

## Dark Mode
Toggles dark mode on and off.

## Floating Macro Panel
Toggles Macro panel floating (always on top) on and off.

## Toggle Axis 1 / Toggle Italic
Toggles between masters across axis number 1 (or 2, 3, 4) or Italic axis (no matter what number it is). Takes into account selected layers in the current tab. Smart enough to toggle special brace layers such as {50, 100, 0} > {50, 100, 15}.

## Demo Instance Generator
Generates instances with limited character set (customizable) from active instances. Adds “Demo” suffix, removes features and OT classes depending on the character set. Needs Vanilla.

## Text Filter
Removes all characters from a text, except selected ones. Useful for testing WIP fonts with limited character set. Needs Vanilla.

## G2 Harmonize
Harmonizes any selected on-curve points. Algorithm found at @simoncozens. Now the same as Green Harmony plugin.

## Dangerous Offcurves
Checks if there are any off-curve points (handles) dangerously close to their curve segment (that may cause problems with conversion to True Type bezier for variable fonts). Opens problematic layers in a new tab. Default threshold value is 0.05 units.

## Point Counter
Shows how many points are there in each layer of the current glyph. Useful for fixing interpolation.

## Kern to max
For the current pair in the edit view, sets the kerning to maximum. Maximum is the half width of the narrower layer in the pair. Useful for kerning (but not overkerning) stuff like .T. or 'A'

## Delete Kerning Pair From All Masters
Removes kerning for selected pair(s) from all masters. If the glyph has a kerning group, it will remove kerning for that group. Exceptions (open locks) are ignored because it’s unclear how to treat them, especially if not all masters have that exception.

## Reorder Shapes
A better algorithm for correcting order of shapes (paths, components). It orders paths by length, y, and x. It orders components by glyph name, y, x.
Works somewhat more reliably than Glyphs' own shape ordering tool.

## Generate Random Alternates Feature
Creates a OpenType feature that randomizes alternatives.
1. Glyphs from selected Categories are randomly added to a selected number of Classes (called rand...).
2. Then glyphs and its alternatives are randomly placed in 'sub... by ...' sequences of the choosen length.
3. That can be repeated a few times, depending on how many lookups and lines per lookup you choose.
Input format: glyph and its alternatives space separated. Next glyph with its alternatives goes to the next line
The script is sketchy. The randomness depends on the numbers choosen, give it a try.

## Fit Zoom
Fits text in current tab into full screen (if Text/Hand tool is selected) or fits current layer (if other tools are being selected). Works weirdly in Glyphs 3. Send help! :)

## Overlap Nodes
Very specific tool that helps to solve kinks on terminals between narrow and normal widths. Converts this:

![image](https://user-images.githubusercontent.com/60325634/136535807-2c6927ad-ac17-4ab0-9ab2-64e8ee0b0668.png)


into this:

![image](https://user-images.githubusercontent.com/60325634/136535872-cb9955f3-7462-4798-9fcf-afa402a0ff8a.png)



### License
Copyright 2020 Alex Slobzheninov.

Some algorithm input by Simon Cozens (@simoncozens).
Floating window code help by Florian Pircher.
Distribute Nodes Horizontally/Vertically are a slightly modified version of Distribute Nodes by Rainer Erich Scheichelbauer (@mekkablue)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use the software provided here except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
