from time import monotonic

class SparklePixel():

    def __init__(self, pixels, location, bright_color, dim_color, speed = 1.0):
        self.pixels = pixels
        self.location = location
        self.bright_color = bright_color
        self.dim_color = dim_color
        self.color_diff = tuple(self.bright_color[rgb] - self.dim_color[rgb] for rgb in range(len(self.bright_color)))

        self.color = self.bright_color

        self.speed = speed

        self.dimming = True
        self.event_start = monotonic()
        self.event_duration = self.speed

    def update(self):
        delta = monotonic() - self.event_start
        if delta > self.event_duration:
            self.event_start += self.event_duration
            delta -= self.event_duration

            #print("Dim change", self.dimming, self.event_start)
            self.dimming = not self.dimming

        ratio = delta / self.event_duration
        if not self.dimming:
            ratio = 1 - ratio

        self.color = tuple(self.dim_color[rgb] + int(ratio*self.color_diff[rgb]) for rgb in range(len(self.dim_color)))
        self.gcolor = tuple(int(pow(self.color[rgb]/255, 2.8) * 255 + 0.5) for rgb in range(len(self.color)))

        #print(color)
        #if self.dimming is True:
            #print("Dimming", ratio, elapsed, self.next_change)
        #else:
            #print("brightening", ratio)

    def sparkle(self, gamma = True):
        color = self.color
        if gamma is True:
            color = self.gcolor

        self.pixels[self.location] = color

