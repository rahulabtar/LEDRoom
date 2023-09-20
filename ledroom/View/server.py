from typing import Tuple
from strip import Strip
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, strip1: Strip, *args, **kwargs) -> None:
        self.strip1 = strip1
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        current_brightness = self.strip1.get_brightness() * 100

        # Generate color dropdown options using COLOR_DICT
        color_options = ""
        for color_name, color_rgb in self.strip1.COLOR_DICT.items():
            color_options += '<option value="{}">{}</option>\n'.format(color_name, color_name)

    # The color dropdown HTML code
        color_dropdown = ''
        for i in range(1, 5):  # Generate four color dropdowns
            color_dropdown += '''
            <label for="color{}">Color {}:</label>
            <select name="color{}">
             {}
            </select>
            <br>
            '''.format(i, i, i, color_options)

    # The main HTML form code
        html = '''
        <html>
        <body 
        style="width:960px; margin: 20px auto;">
        <h1>Welcome to Rahul's Raspberry Pi LED Strip Controller</h1>
        <form action="/" method="POST">
            Strip Options:
            <input type="submit" name="submit" value="Off">
            <br>
            <label for="brightness">Brightness:</label>
            <input type="range" id="brightness" name="brightness" min="1" max="100" value="{}">
            <span>{}</span>%
            <br>
            Strip modes:
            <select name="submit">
            <option value="Off">Turn Strip Off</option>
            <option value="FillColor">Fill a Color, 1 color</option>
            <option value="Twinkle">Twinkle, 4 colors</option>
            <option value="Flow">Flow, 2 colors</option>
            <option value="RainAnim">Rainbow Animation </option>
            <option value="DualCat">Dual Catapillar, 4 colors</option>
            <option value="DayTimeLighting">DayTimeLighting</option>
        </select>
        <br>
        {}
        <input type="submit" value="Update">
    </form>
    </body>
    </html>
    '''.format(current_brightness, round(current_brightness, 3), color_dropdown)

        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("&")  # Split the data into key-value pairs

        action = None
        brightness = None
        selected_colors = [None,None,None,None]  # Initialize the selected color variable

        for key_value in post_data:
            key, value = key_value.split("=")
            if key == "submit":
                action = value
            elif key == "brightness":
                brightness = int(value)
            elif key.startswith("color"):  # Capture the selected colors from the form
                dropdown_index = int(key.split("color")[1]) - 1  # Get the dropdown index (0 to 3)
                selected_colors[dropdown_index] = value

    # Handle the different actions as before
        if action == 'FillColor':
            print(selected_colors)
            self.strip1.fill_color_effect(selected_colors[0])
            print('Fill Color')
        elif action == 'Twinkle':
            print(selected_colors)
            threading.Thread(target=self.strip1.twinkle_effect, args=(selected_colors[0],selected_colors[1],selected_colors[2],selected_colors[3],)).start()
            print("Twinkle")
        elif action == 'Flow':
            threading.Thread(target=self.strip1.flow_effect, args=(selected_colors[0],selected_colors[1],)).start()
            print("Flow")
        elif action == 'DualCat':
            threading.Thread(target=self.strip1.dual_catapillars_effect, args=(selected_colors[0],selected_colors[1],selected_colors[2],selected_colors[3],)).start()
            print("Dual Catapillars")
        elif action == 'RainAnim':
            rainbow_thread = threading.Thread(target=self.strip1.rainbow_animation_effect)
            rainbow_thread.start()
            rainbow_thread.join()  # Wait for the thread to finish before moving on
            print("Rainbow Animation")
        elif action == 'DayTimeLighting':
            threading.Thread(target=self.strip1.day_time_lighting_effect).start()
            print("DayTimeLighting")
        elif action == "Off":
            self.strip1.clear_strip()
            print("OFF Action")

        if brightness is not None:
            self.strip1.set_brightness(brightness / 100)
        print("LED is {}".format(action))
        self._redirect('/')  # Redirect back to the root URL
