import time
import board
import neopixel
import random
import math
import threading
import numpy as np
import colorsys

#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)

class Strip:
    #A dict with all the colors in it, color name key, value decimal rgb
    COLOR_DICT = {
    "Black": (0,0,0),
    "Maroon": (128, 0, 0),
    "Dark_Red": (139, 0, 0),
    "Brown": (165, 42, 42),
    "Firebrick": (178, 34, 34),
    "Crimson": (220, 20, 60),
    "Red": (255, 0, 0),
    "Tomato": (255, 99, 71),
    "Coral": (255, 127, 80),
    "Indian_Red": (205, 92, 92),
    "Light_Coral": (240, 128, 128),
    "Dark_Salmon": (233, 150, 122),
    "Salmon": (250, 128, 114),
    "Light_Salmon": (255, 160, 122),
    "Orange_Red": (255, 69, 0),
    "Dark_Orange": (255, 140, 0),
    "Orange": (255, 165, 0),
    "Gold": (255, 215, 0),
    "Dark_Golden_Rod": (184, 134, 11),
    "Golden_Rod": (218, 165, 32),
    "Pale_Golden_Rod": (238, 232, 170),
    "Dark_Khaki": (189, 183, 107),
    "Khaki": (240, 230, 140),
    "Olive": (128, 128, 0),
    "Yellow": (255, 255, 0),
    "Yellow_Green": (154, 205, 50),
    "Dark_Olive_Green": (85, 107, 47),
    "Olive_Drab": (107, 142, 35),
    "Lawn_Green": (124, 252, 0),
    "Chartreuse": (127, 255, 0),
    "Green_Yellow": (173, 255, 47),
    "Dark_Green": (0, 100, 0),
    "Green": (0, 128, 0),
    "Forest_Green": (34, 139, 34),
    "Lime": (0, 255, 0),
    "Lime_Green": (50, 205, 50),
    "Light_Green": (144, 238, 144),
    "Pale_Green": (152, 251, 152),
    "Dark_Sea_Green": (143, 188, 143),
    "Medium_Spring_Green": (0, 250, 154),
    "Spring_Green": (0, 255, 127),
    "Sea_Green": (46, 139, 87),
    "Medium_Aqua_Marine": (102, 205, 170),
    "Medium_Sea_Green": (60, 179, 113),
    "Light_Sea_Green": (32, 178, 170),
    "Dark_Slate_Gray": (47, 79, 79),
    "Teal": (0, 128, 128),
    "Dark_Cyan": (0, 139, 139),
    "Aqua": (0, 255, 255),
    "Cyan": (0, 255, 255),
    "Light_Cyan": (224, 255, 255),
    "Dark_Turquoise": (0, 206, 209),
    "Turquoise": (64, 224, 208),
    "Medium_Turquoise": (72, 209, 204),
    "Pale_Turquoise": (175, 238, 238),
    "Aqua_Marine": (127, 255, 212),
    "Powder_Blue": (176, 224, 230),
    "Cadet_Blue": (95, 158, 160),
    "Steel_Blue": (70, 130, 180),
    "Corn_Flower_Blue": (100, 149, 237),
    "Deep_Sky_Blue": (0, 191, 255),
    "Dodger_Blue": (30, 144, 255),
    "Light_Blue": (173, 216, 230),
    "Sky_Blue": (135, 206, 235),
    "Light_Sky_Blue": (135, 206, 250),
    "Midnight_Blue": (25, 25, 112),
    "Navy": (0, 0, 128),
    "Dark_Blue": (0, 0, 139),
    "Medium_Blue": (0, 0, 205),
    "Blue": (0, 0, 255),
    "Royal_Blue": (65, 105, 225),
    "Blue_Violet": (138, 43, 226),
    "Indigo": (75, 0, 130),
    "Dark_Slate_Blue": (72, 61, 139),
    "Slate_Blue": (106, 90, 205),
    "Medium_Slate_Blue": (123, 104, 238),
    "Medium_Purple": (147, 112, 219),
    "Dark_Magenta": (139, 0, 139),
    "Dark_Violet": (148, 0, 211),
    "Dark_Orchid": (153, 50, 204),
    "Medium_Orchid": (186, 85, 211),
    "Thistle": (216, 191, 216),
    "Plum": (221, 160, 221),
    "Violet": (238, 130, 238),
    "Orchid": (218, 112, 214),
    "Medium_Violet_Red": (199, 21, 133),
    "Pale_Violet_Red": (219, 112, 147),
    "Deep_Pink": (255, 20, 147),
    "Hot_Pink": (255, 105, 180),
    "White" : (255,255,255),
    "NA" : "NA"
}

    def __init__(self,boardpin:board,num_leds:int,brightness=0.05) -> None:
        self.num_leds = num_leds
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(boardpin, num_leds, brightness=0.05) #has attribute autofill.
        self.flag = 'Off' #The flag helps with switching between modes and threading
        self.effects = {
            'twinkle': self.twinkle_effect,
            'flow': self.flow_effect,
            'dual_cat': self.dual_catapillars_effect,
            'rainbow_anim': self.rainbow_animation_effect,
            'pulse': self.pulse_effect,
            'sin_wave': self.sin_wave_effect,
            'shimmer': self.shimmer_effect,
            'ball': self.bouncing_ball_effect,
            'stars': self.shooting_stars_effect,
            'fire': self.fire_effect,
        }

    def get_brightness(self):
        return self.brightness
    
    def set_brightness(self,brightnessinput:int):
        self.brightness = brightnessinput
        self.pixels.brightness = self.brightness
    
    def run_effect(self, effect_name, wait=20):
        while True:
            print(f'Effect {effect_name}')
            selected_effect = random.choice(list(self.effects.keys()))
            print(selected_effect)

            effect_thread = threading.Thread(target=self.effects[selected_effect])
            effect_thread.start()

            # Wait for the specified duration before transitioning
            time.sleep(wait)

            # Stop the effect based on the selected effect
            self.flag = 'Stop'  # You might need to implement a stopping mechanism in your effect methods
            effect_thread.join()  # Wait for the effect_thread to finish

    def transition_effects(self, wait=20):
        while True:
            for effect_number in range(2):
                effect_name = f'effect{effect_number + 1}'
                self.run_effect(effect_name, wait)

    def get_pixel_color(self,PIXEL_INDEX):
        # Retrieve the RGB decimal value of the specified pixel
        pixel_color = self.pixels[PIXEL_INDEX]
        r, g, b = pixel_color

    def twinkle_effect(self, color1='Red', color2='Yellow', color3='White', color4='Orange', FADE=10, FADE_SPEED = 0.2, TWINKLE_SPEED=0.03):
        """This effect takes in 4 colors and has them randomly twinkle and fade away along the strip"""
        self.flag = 'Twinkle'
        self.pixels.auto_write = False

        palette = [self.COLOR_DICT[color1], self.COLOR_DICT[color2], self.COLOR_DICT[color3], self.COLOR_DICT[color4]]

        def fade_to_black_thread():
            while self.flag == 'Twinkle':
                if FADE != 0:
                    self.fade_to_black(FADE)
                time.sleep(FADE_SPEED)
        fade_thread = threading.Thread(target=fade_to_black_thread)
        fade_thread.start()

        while self.flag == 'Twinkle':
            self.pixels[random.randint(0, self.num_leds - 1)] = palette[random.randint(0, len(palette) - 1)]
            self.pixels.show()
            time.sleep(TWINKLE_SPEED)  # Adjust the time delay to control the twinkle speed

        fade_thread.join()  # Wait for the fading thread to finish

    def flow_effect(self,color1 = 'Red', color2 = 'Violet',wait=1):
        """This effect takes in two colors and alternates them along the strip. Auto_write is off to allow smooth loading and showing.
        The odd and even position colors are switched to give the illusion of a flowing light"""
        self.pixels.auto_write = False
        self.clear_strip()
        self.flag = 'Flow'
        colors = [self.COLOR_DICT[color1],self.COLOR_DICT[color2]]

        while self.flag == 'Flow':
            self.get_pixel_color(5)
            for i in range(0, self.num_leds, 2):
                self.pixels[i] = colors[0]
            for i in range(1, self.num_leds, 2):
                self.pixels[i] = colors[1]
            time.sleep(wait)
            self.pixels.show()

            # Swap colors for the next iteration
            colors[0], colors[1] = colors[1], colors[0]

    def fill_color_effect(self,color='Orange'):
        """ Fills Color"""
        self.clear_strip()
        self.pixels.fill(self.COLOR_DICT[color])
    
    def dual_catapillars_effect(self,color1='Red',color2='Blue',trail1 = 'Yellow', trail2 = 'Green',SLEEP = 0, SPEED = 0.025, FADE = 20, CAT_SIZE = 8,):
        """This effect takes in 4 colors. The first two are the colors of the moving blocks or catapillars. The second two are the colors of the trails they leave behind. The catapillars bounce at the opposite end of the strip then they started at, and disappear once they 
        reach the end of the strip they started at. CAT_SIZE can be adjusted to affect how big they are. Speed can change how fast they travel (lower faster), FADE is how much trail fades, SLEEP is how long strip is black between cycles (zero for none)"""
        self.clear_strip()
        self.flag = 'Dual_Cats'
        self.pixels.auto_write = False

        NUM_LEDS = self.num_leds

        if FADE != 0:
            def fade_to_black_thread():
                while self.flag == 'Dual_Cats':
                        self.fade_to_black(FADE)
                        time.sleep(SPEED)

            fade_thread = threading.Thread(target=fade_to_black_thread)
            fade_thread.start()

        def travel_effect(start_index, color1,color2,trail1,trail2):
            for i in range(start_index, 0, -1):
                self.pixels[i:i+CAT_SIZE] = [color1] * CAT_SIZE
                self.pixels[NUM_LEDS-i:NUM_LEDS-i+CAT_SIZE] = [color2] * CAT_SIZE
                time.sleep(SPEED)
                self.pixels[i:i+CAT_SIZE] = [trail1] * CAT_SIZE
                self.pixels[NUM_LEDS-i:NUM_LEDS-i+CAT_SIZE] = [trail2] * CAT_SIZE


        # Loop through the travel effect with different colors
        while self.flag == 'Dual_Cats':
            travel_effect(NUM_LEDS-CAT_SIZE, self.COLOR_DICT[color1],self.COLOR_DICT[color2],self.COLOR_DICT[trail1],self.COLOR_DICT[trail2])
            self.pixels.fill((0,0,0))
            travel_effect(NUM_LEDS-CAT_SIZE, self.COLOR_DICT[color2],self.COLOR_DICT[color1],self.COLOR_DICT[trail2],self.COLOR_DICT[trail1])
            self.pixels.fill((0,0,0))
            time.sleep(SLEEP)

    def rainbow_animation_effect(self,wait=0.01,mult=3):
        """Shows a slow traveling rainbow, wait and mult help decide how fast travels. Mult still kinda broken so don't touch"""
        self.clear_strip()
        self.flag = 'Rainbow_Animation'
        NUM_LEDS = self.num_leds
        self.pixels.auto_write = False

        while self.flag == 'Rainbow_Animation':
            for j in range(255):
                for i in range(NUM_LEDS):
                    pixel_index = (i * 256 // NUM_LEDS) + j
                    self.pixels[i] = self.wheel(pixel_index & 255,mult)
                time.sleep(wait)
                self.pixels.show()

    def pulse_effect(self, color1='Red', color2='Green', color3='Blue', wait=0.01):
        self.flag = 'pulse'
        color1, color2, color3 = self.COLOR_DICT[color1], self.COLOR_DICT[color2], self.COLOR_DICT[color3]
        black = (0,0,0)
        self.pixels.auto_write = False
        def black():
            time.sleep(1)
            for i in range(17):
                self.fade_to_black()
                time.sleep(0.01)
        def fadecol(colorin):
            for i in range(17):
                self.fade_to_color(colorin)
                time.sleep(0.01)
        while self.flag=='pulse':
            black()
            fadecol(color1)
            black()
            fadecol(color2)
            black()
            fadecol(color3)

    def sin_wave_effect(self,color1='Red', color2 = 'Orange', color3 = 'Yellow', color4 = 'Coral'):
        color1, color2, color3, color4 = self.COLOR_DICT[color1], self.COLOR_DICT[color2], self.COLOR_DICT[color3], self.COLOR_DICT[color4]
        colors = [color1,color2,color3,color4]
        self.clear_strip()
        self.flag = 'sin_wave'
        self.pixels.auto_write = False

        def fade_to_black_thread():
            while self.flag == 'sin_wave':
                self.fade_to_black()
                time.sleep(0.05)

        fade_thread = threading.Thread(target=fade_to_black_thread)
        fade_thread.start()

        strip_length = self.num_leds
        block_position = 0
        direction = 1  # 1 for moving right, -1 for moving left
        block_size = 3

        # Initialize extra streaks
        num_streaks = 4  # Number of extra streaks
        streaks = []

        for _ in range(num_streaks):
            frequency = random.randint(5, 10)  # Adjust the frequency range as needed
            phase_offset = random.uniform(0, 2 * 3.14159)  # Random phase offset
            color = colors[_]
            streaks.append((frequency, phase_offset, color))

        while self.flag == 'sin_wave':
            # Extra streaks of light
            for streak in streaks:
                frequency, phase_offset, color = streak
                position = int(self.beatsin8(frequency, 0, strip_length - 1, time.time(), phase_offset))
                self.pixels[position] = color

            self.pixels.show()

            block_position += direction
            if block_position + block_size >= strip_length or block_position <= 0:
                direction *= -1  # Reverse direction at the ends

            time.sleep(0.01)  # Adjust speed

    def shimmer_effect(self,color=(0,255,0)):
        self.pixels.auto_write = False
        self.flag = 'shimmer'
        def ColorFromPalette(palette, index, brightness):
            color = palette[index % len(palette)] 
            return (
                color[0] * brightness // 255,
                color[1] * brightness // 255,
                color[2] * brightness // 255
            )

        palette = self.generate_color_palette(color,4)

        # Initialize colorIndex array with random values
        colorIndex = [random.randint(0, 255) for _ in range(self.num_leds)]

        last_time = time.time()
        animation_interval = 1 

        # Main loop
        while self.flag == 'shimmer':
            current_time = time.time()
            time_elapsed = current_time - last_time

            if time_elapsed >= animation_interval:
                last_time = current_time

                t = current_time  # Use the current time for animation
        
                # Create a sin wave with a period of 2 seconds (30bpm) to change the brightness
        
            # Color each pixel from the palette using the index from colorIndex[]
            for i in range(self.num_leds):
                t = current_time
                color = ColorFromPalette(palette, colorIndex[i], self.beatsin8(30, 120, 255, t, 0))
                self.pixels[i] = color
        
            for i in range(self.num_leds):
                colorIndex[i] = (colorIndex[i] + 1) % len(palette)
        
            self.pixels.show()
    
    def bouncing_ball_effect(self, color=(0, 0, 255), gravity=1, initial_velocity=5):
        self.pixels.auto_write = False
        self.flag = 'bouncing_ball'
        def fade_to_black_thread():
            while True:
                self.fade_to_black(20)
                time.sleep(0.01)

        fade_thread = threading.Thread(target=fade_to_black_thread)
        fade_thread.start()

        NUM_LEDS = self.num_leds
        restart_interval = 10  # Set the restart interval in seconds

        while self.flag== 'bouncing_ball':
            # Randomize gravity and initial velocity
            gravity = random.uniform(0.5, 1.5)  # Adjust the range as needed
            initial_velocity = random.uniform(3, 7)  # Adjust the range as needed

            position = 0
            velocity = initial_velocity
            dampen_velocity = (random.randint(50,80)/100)
            #print(dampen_velocity)
            ball_colors = self.get_more_colors(color)

            start_time = time.time()
            
            while position >= 0:
                # Clear the LED strip

                # Update the position based on velocity and gravity
                position += velocity
                velocity += gravity

                # If the ball reaches the ground, reverse direction and dampen velocity
                if position >= NUM_LEDS - 1:
                    position = NUM_LEDS - 1
                    velocity = -velocity * dampen_velocity  # Dampen velocity (change the factor as needed)

                # Set the pixel at the current position to the ball color
                self.pixels[int(position)] = ball_colors[int(position) % 4]

                # Show the updated LED strip
                self.pixels.show()

                # Delay to control the animation speed (adjust as needed)
                time.sleep(0.05)

                # Check if it's time to restart the animation
                if time.time() - start_time >= restart_interval:
                    break

            # Sleep for a couple of seconds before starting a new animation
            time.sleep(2)

    def shooting_stars_effect(self, base_color=(0, 0, 255)):
        self.pixels.auto_write = False
        self.flag = 'shooting_stars'

        def fade_to_black_thread():
            while self.flag=='shooting_stars':
                self.fade_to_black(20)
                time.sleep(0.01)

        fade_thread = threading.Thread(target=fade_to_black_thread)
        fade_thread.start()
        colors = self.get_more_colors(base_color)


        def spawn_pixel(color_pix):
            #colors = self.get_more_colors(base_color) #gets list of complementary colors
            
            #print(new_color)
            for i in range(self.num_leds):
                # Generate a random color variation from the base_color
                if self.flag == 'shooting_stars':
                    self.pixels[i] = color_pix
                    time.sleep(0.03)

        while self.flag == 'shooting_stars':
            index = random.randint(0,3)
            thread = threading.Thread(target=spawn_pixel, args = (colors[index],))
            thread.start()
            time.sleep(1.5)  # Adjust the interval between new pixels     

    def fire_effect(self):
        self.pixels.auto_write=False
        NUM_LEDS = self.num_leds
        cooling = 50
        sparking = 240
        heat = [0] * NUM_LEDS
        self.flag = 'fire'

        def fire_loop():
            # Step 1: Cool down every cell a little
            for i in range(NUM_LEDS):
                heat[i] = max(0, heat[i] - random.randint(0, ((cooling * 10) // NUM_LEDS) + 2))

            # Step 2: Heat from each cell drifts 'up' and diffuses a little
            for k in range(NUM_LEDS - 1, 1, -1):
                heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) // 3
            
            # Step 3: Randomly ignite new 'sparks' of heat near the bottom
            if random.randint(0, 255) < sparking:
                y = random.randint(0, 6)
                heat[y] = min(255, heat[y] + random.randint(160, 255))

            # Step 4: Map from heat cells to LED colors
            for j in range(NUM_LEDS):
                custom_fire_color = (10, 150, 100) #manip to change coor
                #color = heat_color(heat[j],custom_fire_color)
                color = heat_color(heat[j])
                self.pixels[j] = color

        def heat_color(temperature, custom_color=None):
            temperature = min(temperature, 255)
            temperature = max(temperature, 0)
    
            if custom_color != None:
                # Adjust the custom color based on temperature for a fire-like effect
                r, g, b = custom_color
                r = min(255, r + temperature // 3)
                g = min(255, g + temperature // 6)
                b = max(0, b - temperature // 3)  # Decrease blue for fire effect

                return (r, g, b)

            # Default color mapping with less green and blue
            if temperature < 128:
                r = temperature * 2
                g = temperature // 2
                b = 0
            else:
                r = 255
                g = 255 - ((temperature - 128) // 2)
                b = max(0,(temperature - 128 // 4))

            return (r, g, b)


        while self.flag=='fire':
            fire_loop()
            self.pixels.show()
            time.sleep(0.03)  # Adjust the delay to control the animation speed

    def fade_to_black(self, FADE=15):
       # """This method causes the entire strip to slowly fade to black by a specified amount."""
        for i in range(self.num_leds):
                r, g, b = self.pixels[i]
                r = max(0, r - FADE)
                g = max(0, g - FADE)
                b = max(0, b - FADE)
                self.pixels[i] = (r, g, b)
        self.pixels.show()

    def fade_to_color(self, target_color, FADE=15):
        # This method causes the entire strip to slowly fade to the specified color by a specified amount.
        for i in range(self.num_leds):
            r, g, b = self.pixels[i]
            tr, tg, tb = target_color
            r = min(tr, r + FADE)  # Increase/decrease brightness while avoiding overflow/underflow
            g = min(tg, g + FADE)
            b = min(tb, b + FADE)
            self.pixels[i] = (r, g, b)
        self.pixels.show()

    def beatsin8(self,beats_per_minute, min_value, max_value, time_value,phase_offset =0):
        """
        Simulates the beatsin8 function from FastLED.
        beats_per_minute: Beats per minute (frequency of oscillation)
        min_value: Minimum value of the wave
        max_value: Maximum value of the wave
        time_value: Current time value
        """
        bpm = beats_per_minute / 60.0
        delta = math.sin(time_value * bpm * 2 * math.pi + phase_offset) * 0.5 + 0.5
        return int(min_value + delta * (max_value - min_value))
    
    def wheel(self,pos,mult=3):

        """This method takes in a position along the strip and returns RGB values, usually for a rainbow wheel effect. mult helps determine these colors"""
        # Input a value 0 to 255 to get a color value.
        # The colors are a transition from red to green to blue and back to red.
        if pos < 85:
            return (255 - pos * mult, pos * mult, 0)
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * mult, pos * mult)
        else:
            pos -= 170
            return (pos * mult, 0, 255 - pos * mult)

    def clear_strip(self):
        """This method clears the strip and the flag to allow transitions between affects"""
        self.flag = 'Clear'
        self.pixels.fill((0,0,0))

    def get_more_colors(self,input_color):
        r, g, b = [x / 255.0 for x in input_color]

        # Convert RGB to HSV (Hue, Saturation, Value)
        hsv = colorsys.rgb_to_hsv(r, g, b)

        # Calculate analogous colors by varying the hue
        analogous_colors = [input_color]
        for offset in [-30, 30, 60]:  # You can adjust these offsets
            new_hue = (hsv[0] + offset/360.0) % 1.0
            r, g, b = colorsys.hsv_to_rgb(new_hue, hsv[1], hsv[2])
            # Convert back to 8-bit RGB values (0-255)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            analogous_colors.append((r, g, b))
        return analogous_colors

    def generate_color_palette(self,base_color, num_colors):
        # Convert the input RGB color to HSV (Hue, Saturation, Value)
        base_hsv = colorsys.rgb_to_hsv(base_color[0] / 255.0, base_color[1] / 255.0, base_color[2] / 255.0)

        # Initialize an empty list to store the palette colors
        palette = []

        # Calculate the hue step size to create similar colors
        hue_step = 0.05

        # Generate similar colors by varying the hue while keeping saturation and value constant
        for i in range(num_colors):
            hue = (base_hsv[0] + i * hue_step) % 1.0  # Ensure hue stays within [0, 1]
            rgb_color = colorsys.hsv_to_rgb(hue, base_hsv[1], base_hsv[2])
            rgb_color = tuple(int(x * 255) for x in rgb_color)  # Convert back to 8-bit RGB values
            palette.append(rgb_color)

        return palette

#stripex = Strip(board.D21,300,0.05)
#stripex.transition_effects()
#stripex.flow_effect()
#stripex.blend_effects()
#stripex.clear_strip()
#stripex.twinkle_effect()
#stripex.fill_color_effect()
#stripex.dual_catapillars_effect() 
#stripex.rainbow_animation_effect()
#stripex.pulse_effect() 
#stripex.sin_wave_effect() 
#stripex.shooting_stars_effect() 
#stripex.bouncing_ball_effect() 
#stripex.generate_color_palette((0,255,245),4)
#stripex.shimmer_effect((100,0,255))
#stripex.get_more_colors((0,255,0))