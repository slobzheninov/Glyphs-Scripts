## About

These are scripts for [Glyphs](https://glyphsapp.com/). Some may not work in Glyphs 3, WIP.

### Installation: 
Put the scripts into Scripts folder: Library – Application Support - Glyphs - Scripts
(Cmd + Shift + Y) or through Plugin Manager in Glyphs 3.

### Align, Reflect and Rotate
Align and reflect nodes and handles. Useful with keyboard shortcuts — I personally use Ctrl + Cmd + Arrow keys. Set it in System Preferences – Keyboard – Shortcuts.

Center Selected Glyphs sets equal left and right sidebearings within the same width for all layers of selected glyphs.

### Preferred Names
Sets (or cleans) *preferredFamily* and *preferredSubfamily* instance custom parameters. Based on *Font Family Name* and *Instance / Style Name*. Useful for office apps compatibility.

### Dark Mode
Toggles dark mode on and off.

### Toggle Axis 1
Toggles between masters across axis number 1 (or 2, 3, 4) in current tab.

### Toggle Italic
Toggles between upright and italic masters in current tab. Expects that italic and upright masters have the same axes values, except for different 'ital' or 'slnt'.
I use it with cmd+§. Same as Toggle Axis N, except for it doesn't care what number italic axis is.

### Demo Instance Generator
Generates instances with limited character set (customizable) from active instances. Adds “Demo” suffix, removes features and OT classes depending on the character set.

### Text Filter
Removes all characters from a text, except selected ones. Useful for testing WIP fonts with limited character set.

### G2 Harmonize
Harmonizes any selected on-curve points. Algorithm found at @simoncozens. Now the same as Green Harmony plugin.

### Dangerous Offcurves
Checks if there are any off-curve points (handles) dangerously close to their curve segment (that may cause problems with conversion to True Type bezier for variable fonts). Opens problematic layers in a new tab. Default threshold value is 0.05 units.

### Point Counter
Shows how many points are there in each layer of the current glyph. Useful for fixing interpolation.

### Overlap Nodes
Very specific tool that helps to solve kinks on terminals between narrow and normal widths. Converts this:

![image](https://user-images.githubusercontent.com/60325634/136535807-2c6927ad-ac17-4ab0-9ab2-64e8ee0b0668.png)


into this:

![image](https://user-images.githubusercontent.com/60325634/136535872-cb9955f3-7462-4798-9fcf-afa402a0ff8a.png)



### License
Copyright 2020 Alex Slobzheninov.

Some algorithm input by Simon Cozens (@simoncozens).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use the software provided here except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
