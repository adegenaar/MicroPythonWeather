import time
import neopixel
from machine import Pin


class Colors:
    """
     pre-built color defintions
    """

    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.gold = (75, 115, 0)


class animations:
    """
     various animation routines for NeoPixels
    """

    def __init__(self, np=None, ledPin=2, ledCount=20):
        """
        __init__ Constructor

        Args:
            np (NeoPixel Object, optional): Used to pass an already created NeoPixel Object. Defaults to None.
            ledPin (int, optional): GPIO Pin connected to the NeoPixels.  Must support PWM. Defaults to 2.
            ledCount (int, optional): Number of LED Pixels in the strip. Defaults to 20.
        """
        if np is None:
            self._ledPin = ledPin
            self.np = neopixel.NeoPixel(Pin(ledPin), ledCount)
        else:
            self._ledPin = ledPin

    def setcolor(self, color):
        """
        setcolor Set the entire strip to a single color

        Args:
            color (tuple): rgb tuple
        """
        for j in range(self.np.n):
            self.np[j] = color
            self.np.write()

    def clear(self):
        """
        clear - Convenience function to set the strip to off (0,0,0) 
        """
        self.setcolor(self.np, Colors.black)

    def cycle(self, color=Colors.white, wait=25):
        """
        cycle - Sequential single pixel animation 

        Args:
            color (tuple, optional): Color to use for the animated pixel. Defaults to Colors.white.
            wait (int, optional): time to wait between cycle progressions. Defaults to 25ms.
        """
        n = self.np.n

        # cycle
        for i in range(n):
            self.clear(self.np)
            self.np[i % n] = color
            self.np.write()
            time.sleep_ms(wait)

    def bounce(self, color=Colors.white, wait=60):
        """
        bounce - Opposite of Cycle, one dark pixel cycles around the NeoPixel strip

        Args:
            color (tuple optional): Color for the strip. Defaults to Colors.white.
            wait (int, optional): Time to wait between cycle progessions. Defaults to 60ms.
        """
        # bounce
        for i in range(4 * self.np.n):
            self.setcolor(color)
            if (i // self.np.n) % 2 == 0:
                self.np[i % self.np.n] = Colors.black
            else:
                self.np[self.np.n - 1 - (i % self.np.n)] = Colors.black
            self.np.write()
            time.sleep_ms(wait)

    # TODO: fix this to be more general
    def fade(self, color=Colors.white):
        # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(self.np.n):
                if (i // 256) % 2 == 0:
                    val = i & 0xFF
                else:
                    val = 255 - (i & 0xFF)
                self.np[j] = (val, 0, 0)
            self.np.write()

    def breathe(self):
        """
        breathe - Cycles the strip up and down. 
                  Original version written by: Jason Yandell     
       """
        from math import sin

        MaximumBrightness = 255.0
        SpeedFactor = 0.008  # I don't actually know what would look good
        StepDelay = 5  # ms for a step delay on the lights

        # Make the lights breathe
        for i in range(65535):
            # Intensity will go from 10 - MaximumBrightness in a "breathing" manner
            intensity = MaximumBrightness / 2.0 * (1.0 + sin(SpeedFactor * i))

            # strip.setBrightness(intensity);
            # // Now set every LED to that color
            for ledNumber in range(self.np.n):
                # adjust the brightness
                r = intensity * (self.np[ledNumber][0]) / 255
                g = intensity * (self.np[ledNumber][1]) / 255
                b = intensity * (self.np[ledNumber][2]) / 255
                self.np[ledNumber] = (r, g, b)
            self.np.write()
            time.sleep_ms(StepDelay)

    def _wheel(self, pos):
        """
        _wheel Transitions a color value around the rainbow.  
            Input a value 0 to 255 to get a color value.
            The colours are a transition r - g - b - back to r.
        Args:
            pos (color): color value to trainsition to the next value

        Returns:
            tuple: next color value in the cycle
        """

        if pos < 0 or pos > 255:
            return Colors.black
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, wait):
        """
        rainbow_cycle - Animated rainbow cycle

        Args:
            wait (int): time in ms to wait between each cycle step
        """
        for j in range(255):
            for i in range(self.np.n):
                rc_index = (i * 256 // self.np.n) + j
                self.np[i] = self._wheel(rc_index & 255)
            self.np.write()
            time.sleep_ms(wait)

    def flicker(self, color=self.np[0], step=3, stepsize=10, wait=25):
        """
        flicker - Animated quick 3 step fade and brighten back to the original color 

        Args:
            color (tuple): base color to start from
            step (int, optional): number of steps to fade the color. Defaults to 3.
            stepsize (int, optional): how much should the color change at each step. Defaults to 10.
            wait (int, optional): Time in ms between each step. Defaults to 25ms.
        """
        r = color[0]
        g = color[1]
        b = color[2]

        self.setcolor(r, g, b)
        time.sleep_ms(wait)

        for i in range(step):  # fade down
            r -= stepsize
            g -= stepsize
            b -= stepsize
            if r < 0:
                r = 0
            if g < 0:
                g = 0
            if b < 0:
                b = 0
            self.setcolor(r, g, b)
            time.sleep_ms(wait)

        for i in range(step):  # fade up
            r += stepsize
            g += stepsize
            b += stepsize
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
            self.setcolor(r, g, b)
            time.sleep_ms(wait)

    def color(self, r, g, b):
        """
        color turn an rgb value into a tuple

        Args:
            r (int): Red value
            g (int): Green value
            b (int): Blue value

        Returns:
            tuple : Color value as tuple
        """
        return (r, g, b)

    def blueFlicker(self):
        """
        blueFlicker Flicker animation in Blue
        """
        self.flicker((0, 0, 90))

    def redFlicker(self):
        """
        redFlicker Flicker animation in Red
        """
        self.flicker((0, 90, 0))

    def goldFlicker(self):
        """
        goldFlicker Flicker animation in Gold
        """
        self.flicker(Colors.gold)

    def lightning(self, step=6, wait=25):
        """
        lightning Animation to simulate lightning

        Args:
            step (int, optional): Number of flashes. Defaults to 6.
            wait (int, optional): Time in ms between each flash. Defaults to 25 ms.
        """
        strip = list(self.np)

        for i in range(
            step
        ):  # flicker rapidly between white, black and the original colors
            self.setcolor(Colors.white)
            time.sleep_ms(wait)
            self.setcolor(Colors.black)
            time.sleep_ms(wait)
            for j in range(self.np.n):
                self.np[j] = strip[j]
                self.np.write()
            time.sleep_ms(wait * 2)

    def demo(self):
        """
        demo Run each of the animations in sequence
        """
        # cycle(np)
        # time.sleep(1)
        # cycle(np,red)
        # time.sleep(1)
        # cycle(np,blue)
        # time.sleep(1)
        # cycle(np,gold)
        # time.sleep(1)
        # cycle(np,green)
        # time.sleep(1)
        # clear(np)

        # bounce(np)
        # time.sleep(1)
        # bounce(np,red)
        # time.sleep(1)
        # bounce(np,blue)
        # time.sleep(1)
        # bounce(np,gold)
        # time.sleep(1)
        # bounce(np,green)
        # time.sleep(1)

        # fade(np)
        self.redFlicker()
        self.blueFlicker()
        self.flicker(Colors.green)
        self.goldFlicker()

        self.clear()
        self.rainbow_cycle(60)
        self.lightning()

        colors = [Colors.red, Colors.blue, Colors.green, Colors.gold]
        for c in colors:
            self.setcolor(c)
            self.lightning()

        self.clear()
