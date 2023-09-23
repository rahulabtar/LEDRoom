import board
import neopixel
import time
import random

# Configuration
NUM_LEDS = 50  # Change this to match your NeoPixel strip's number of pixels
PIN = board.D21  # Change this to match the GPIO pin your NeoPixels are connected to

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(PIN, NUM_LEDS, brightness = 0.05, auto_write=False)

source1 = [(0, 0, 0)] * NUM_LEDS  # Initialize source1 with black (off)
print('Initialized')
source2 = [(0, 0, 0)] * NUM_LEDS  # Initialize source2 with black (off)
output = [(0, 0, 0)] * NUM_LEDS  # Initialize output with black (off)
blendAmount = 0
patternCounter = 0
source1Pattern = 0
source2Pattern = 1
useSource1 = False

def setup():
    # Initialize NeoPixel strip
    pixels.show()
    pixels.brightness = 0.5
    print("Initialized NeoPixel strip")

def loop():
    global blendAmount, patternCounter, source1Pattern, source2Pattern, useSource1
    while True:
        blend(source1, source2, output, NUM_LEDS, blendAmount)

        if useSource1:
            if blendAmount < 255:
                blendAmount += 1
        else:
            if blendAmount > 0:
                blendAmount -= 1

        if time.time() % 5 == 0:
            nextPattern()

        runPattern(source1Pattern, source1)
        runPattern(source2Pattern, source2)

        for i in range(NUM_LEDS):
            pixels[i] = output[i]

        pixels.show()
        time.sleep(0.01)  # Adjust the delay as needed

def nextPattern():
    global patternCounter, source1Pattern, source2Pattern, useSource1
    patternCounter = (patternCounter + 1) % 3

    if useSource1:
        source1Pattern = patternCounter
    else:
        source2Pattern = patternCounter

    useSource1 = not useSource1

def runPattern(pattern, LEDArray):
    if pattern == 0:
        movingDots(LEDArray)
    elif pattern == 1:
        rainbowBeat(LEDArray)
    elif pattern == 2:
        redWhiteBlue(LEDArray)

def blend(source1, source2, output, num_leds, blend_amount):
    for i in range(num_leds):
        r1, g1, b1 = source1[i]
        r2, g2, b2 = source2[i]
        r = int((r1 * (255 - blend_amount) + r2 * blend_amount) / 255)
        g = int((g1 * (255 - blend_amount) + g2 * blend_amount) / 255)
        b = int((b1 * (255 - blend_amount) + b2 * blend_amount) / 255)
        output[i] = (r, g, b)

def movingDots(LEDarray):
    posBeat = random.randint(0, NUM_LEDS - 1)
    posBeat2 = random.randint(0, NUM_LEDS - 1)
    posBeat3 = random.randint(0, NUM_LEDS - 1)
    posBeat4 = random.randint(0, NUM_LEDS - 1)
    colBeat = random.randint(0, 255)

    LEDarray[(posBeat + posBeat2) // 2] = (colBeat, 255, 255)
    LEDarray[(posBeat3 + posBeat4) // 2] = (colBeat, 255, 255)

    for i in range(NUM_LEDS):
        r, g, b = LEDarray[i]
        r = max(0, r - 10)
        g = max(0, g - 10)
        b = max(0, b - 10)
        LEDarray[i] = (r, g, b)

def rainbowBeat(LEDarray):
    beatA = random.randint(0, 255)
    beatB = random.randint(0, 255)
    for i in range(NUM_LEDS):
        LEDarray[i] = (beatA + beatB) // 2

    # Update source2 with RGB tuples
    for i in range(NUM_LEDS):
        source2[i] = (beatA, beatB, (beatA + beatB) // 2)

def redWhiteBlue(LEDarray):
    sinBeat = random.randint(0, NUM_LEDS - 1)
    sinBeat2 = random.randint(0, NUM_LEDS - 1)
    sinBeat3 = random.randint(0, NUM_LEDS - 1)

    LEDarray[sinBeat] = (0, 0, 255)  # Blue
    LEDarray[sinBeat2] = (255, 0, 0)  # Red
    LEDarray[sinBeat3] = (255, 255, 255)  # White

    # Update source2 with RGB tuples
    source2[sinBeat] = (0, 0, 255)
    source2[sinBeat2] = (255, 0, 0)
    source2[sinBeat3] = (255, 255, 255)


if __name__ == "__main__":
    pixels.fill((0,0,0))
    setup()
    loop()
