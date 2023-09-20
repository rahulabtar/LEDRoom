import board
import neopixel
import random
import time

NUM_LEDS = 20
DATA_PIN = board.D18
BRIGHTNESS = 0.05


pixels = neopixel.NeoPixel(DATA_PIN, NUM_LEDS, brightness=BRIGHTNESS)

# Defines the gradient palette
palette = [
    (0, 0, 0),        # black
    (255, 0, 0),      # red
    (255, 255, 0),    # bright yellow
    (255, 255, 255),  # full white
]

def loop():
    while True:
        pixels[random.randint(0, NUM_LEDS - 1)] = palette[random.randint(0, len(palette) - 1)]
        fade_to_black()

        pixels.show()
        time.sleep(0.01)  # Adjust the time delay to control the twinkle speed

def fade_to_black():
    for i in range(NUM_LEDS):
        r, g, b = pixels[i]
        r = max(0, r - 1)
        g = max(0, g - 1)
        b = max(0, b - 1)
        pixels[i] = (r, g, b)

if __name__ == '__main__':
    loop()
