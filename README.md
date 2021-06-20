## About

These are scripts for [Glyphs](https://glyphsapp.com/). Some may not work in Glyphs 3, WIP.

### Installation: 
Put the scripts into Scripts folder: Library – Application Support - Glyphs - Scripts
(Cmd + Shift + Y)

### Align, Reflect and Rotate

Align and reflect nodes and handles. Useful with keyboard shortcuts — I personally use Ctrl + Cmd + Arrow keys. Set it in System Preferences – Keyboard – Shortcuts.

### Preferred Names
Sets (or cleans) *preferredFamily* and *preferredSubfamily* instance custom parameters. Based on *Font Family Name* and *Instance / Style Name*. Useful for office apps compatibility.

### Dark Mode
Toggles dark mode on and off.

### Demo Instance Generator
Generates instances with limited character set (customizable) from active instances. Adds “Demo” suffix, removes features and OT classes depending on the character set.

### Text Filter
Removes all characters from a text, except selected ones. Useful for testing WIP fonts with limited character set.

### Dangerous Offcurves
Checks if there are any off-curve points (handles) dangerously close to their curve segment (that may cause problems with conversion to True Type bezier for variable fonts). Opens problematic layers in a new tab. Default threshold value is 0.05 units.




### License
Copyright 2020 The slobzheninov Glyphs-Scripts Project Authors.

Some algorithm input by Simon Cozens (@simoncozens).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use the software provided here except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
