## About

These are scripts for [Glyphs](https://glyphsapp.com/).

### Installation: 
Put the scripts into Scripts folder: Library – Application Support - Glyphs - Scripts
(Cmd + Shift + Y)

### Align and Reflect

Align and reflect nodes and handles. Useful with keyboard shortcuts — I personally use Ctrl + Cmd + Arrow keys. Set it in System Preferences – Keyboard – Shortcuts.

### Mirror Kerning
Mirrors kerning for symmetrical things like AVA or OVO, etc. You control what to mirror.

*Save or create a backup copy before using! It might crash Glyphs.*

Using:
Add a bar symbol (|) to both left and right kerning group names if you want them to mirror. For example @|A or @|V. Kern one side (AV), run the script and get the other side kerned (VA). If both sides already have different kerning values, it’ll open a new tab for you to check. The script igonres uppercase to lowercase mirroring. Don’t forget to put asymmetric glyphs like “b” to apropriate mirroring groups as well!

### Preferred Names
Sets (or cleans) *preferredFamily* and *preferredSubfamily* instance custom parameters. Based on *Font Family Name* and *Instance / Style Name*. Useful for office apps compatibility.

### Dark Mode
Toggles dark mode on and off.

### Demo Instance Generator
Generates instances with limited character set (customizable) from active instances. Adds “Demo” suffix, removes features and OT classes depending on the character set.

### Text Filter
Removes all characters from a text, except selected ones. Useful for testing WIP fonts with limited character set.
