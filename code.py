import time
import board
import math
import random

import adafruit_neopxl8
from adafruit_pixelmap import PixelMap

import adafruit_fancyled.adafruit_fancyled as fancy
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap

from pyicle import Icicle
from sparkle_pixel import SparklePixel
from snow import Snow

# Set up the pixel matrix (15 wide x 20 high)
pixels = adafruit_neopxl8.NeoPxl8(board.A3, 300, brightness=0.3, num_strands=1, bpp=4, auto_write=False)
pixels.fill(0)
pixels.show()

a=()
for x in range(0,300,20):
    if x % 40:
        a += tuple(i for i in range(0+x, 20+x))
    else:
        a += tuple(i for i in range(19+x, -1+x, -1))

m = PixelMap(pixels, a, individual_pixels=True)

# Set up icicles for icicle routine
icicles = []
for i in range(15):
    icicles.append(Icicle(m, column=i, dribblePixel=random.randint(1,3)))
    icicles[i].g_const=3.0+(random.random()*2.0)

# Load font and set up scroling text messages
font = bitmap_font.load_font("SourceSerifPro-Bold-24.pcf", Bitmap)
labels = []
labels.append(Label(text="Happy Holidays!   ", font=font))
labels.append(Label(text="Merry Christmas!    ", font=font))

# Set colors for scrolling text
k = 1.6
hues = [ (complex(0.5+math.sin((x/100)*3.1415-3.1415/2)/2)**((2*(1-(x/100)))**k)).real for x in range(0,200,2)]

YELLOW = fancy.CRGB(1.0,0.5,0)
BLUE = fancy.CRGB(0,0,1.0)
RED = fancy.CRGB(1.0,0,0)
GREEN = fancy.CRGB(0,1.0,0)
colors = [0, 0]

def load_tree(filename):
    """Load tree image and display. Tree is in a raw RGB files format."""
    with open(filename, "rb") as fp:
        x = y = 0

        while True:
            rb = fp.read(1)
            if not rb:
                break
            gb = fp.read(1)
            bb = fp.read(1)
            r = int.from_bytes(rb,"big")
            g = int.from_bytes(gb,"big")
            b = int.from_bytes(bb,"big")

            # gamma adjust
            r = int(pow(r/255, 2.8) * 255 + 0.5)
            g = int(pow(g/255, 2.8) * 255 + 0.5)
            b = int(pow(b/255, 2.8) * 255 + 0.5)

            m[x*20+y] = (r,g,b)
            x = x + 1
            if x == 15:
                x = 0
                y = y + 1

def load_lights(lights):
    """Create lights on the tree image."""
    for _ in range(25):
        while True:
            x = random.randint(0,14)
            if _ < 14:
                y = _ + 3
            else:
                y = random.randint(6,16)

            color = m[x*20+y]
            if color[0] < 50 and color[1] > 200:
                break

        cc = random.randint(0,3)
        if cc == 0:
            bright = (255,0,0)
            dim = (100,0,0)
        elif cc ==1:
            bright = (0,0,255)
            dim = (0,0,100)
        elif cc == 2:
            bright = (255,0,255)
            dim = (100,0,100)
        elif cc == 3:
            bright = (250,250,0)
            dim = (100,100,0)

        sparkle = SparklePixel(m, x*20+y, bright, dim, speed=random.uniform(0.5, 2.5))
        lights.append(sparkle)

def show_tree(delay):
    """Show the tree and sparkle the lights and star and move the snow."""
    lights = []
    m.fill(0)
    m.show()

    load_tree("tree2.rgb")
    load_lights(lights)

    starpoints = [
        SparklePixel(m, 7*20, (255,255,0), (100,100,0), speed=1.5),
        SparklePixel(m, 6*20+1, (255,255,0), (100,100,0), speed=0.8),
        SparklePixel(m, 7*20+1, (255,255,0), (100,100,0), speed=2.5),
        SparklePixel(m, 8*20+1, (255,255,0), (100,100,0), speed=1.0),
        SparklePixel(m, 7*20+2, (255,255,0), (100,100,0), speed=1.25)
    ]

    # Create snowflakes to fall
    snow = []
    for column in range(15):
        if column not in (6, 7, 8):
            s = Snow(m, column, speed = random.uniform(0.2, 0.5))
            snow.append(s)
            s = Snow(m, column, speed = random.uniform(0.2, 0.5))
            snow.append(s)

    end = time.monotonic() + delay
    while time.monotonic() < end:
        for star in starpoints:
            star.update()
            star.sparkle()
        for light in lights:
            light.update()
            light.sparkle()
        for s in snow:
            s.update()

        m.show()

def IcicleShow(delay):
    """Animate icicles for a period of time."""
    end = time.monotonic() + delay
    while time.monotonic() < end:
        m.fill(0)
        for icicle in icicles:
            icicle.draw()
        m.show()


def ScrollOnce(label):
    bitmap = label.bitmap
    hue = random.randint(0,99)
    for i in range(bitmap.width):
        # Use a rainbow of colors, shifting each column of pixels
        #hue = hue + 7
        #if hue >= 256:
            #hue = hue - 256
        #colors[1] = colorwheel(hue)
        hue = hue + 1
        if hue >= 100:
            hue = hue-100
        colors[1] = fancy.mix(RED,GREEN,hues[hue]).pack()

        # Scoot the old text left by 1 pixel
        m[0:280] = m[20:300]

        # Draw in the next line of text
        for y in range(0,20):
            # Select black or color depending on the bitmap pixel
            m[280+y] = colors[bitmap[i,y+2]]
        pixels.show()
        time.sleep(0.04)

# Main loop
labels_index = 0
while True:
    show_tree(30)

    ScrollOnce(labels[labels_index])
    ScrollOnce(labels[labels_index])

    labels_index += 1
    if labels_index >= len(labels):
        labels_index = 0

    for icicle in icicles:
        icicle.resettime()

    IcicleShow(30)

    ScrollOnce(labels[labels_index])
    ScrollOnce(labels[labels_index])

    labels_index += 1
    if labels_index >= len(labels):
        labels_index = 0
