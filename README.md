# Christmas LEDs

Show animations on a 15 wide by 20 high LED matrix.

Animations are:
1. Scrolling text
2. Christmas tree with sparkling lights and star
3. Dripping icicles

The project uses a RP2040 based processor to use the fast adafruit_neopxl8 library. The regular neopixel library could be used but the animations will be slower.

Icicles based on: https://github.com/gamblor21/pyicle

Source Serif Pro from Google Fonts and converted for CircuitPython.

`tree.rgb` is a 15x20 graphic saved in RGB format (one byte per color).
