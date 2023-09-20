import os
import neopixel
import board
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

host_name = '10.69.0.114'  # IP Address of Raspberry Pi
host_port = 8000

pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=0.05)

def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp

class MyServer(BaseHTTPRequestHandler):
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
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to Rahul's Raspberry Pi LED Strip Controller</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Strip Options:
               <input type="submit" name="submit" value="AllRed">
               <input type="submit" name="submit" value="RGBFlash">
               <input type="submit" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = getTemperature()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        if post_data == 'AllRed':
            pixels1.fill((100, 100, 0))
            print('AllRed Mode active')
        elif post_data == 'RGBFlash':
            print("RGBFlash")
            flashing_thread = threading.Thread(target=self._run_flashing)
            flashing_thread.start()
        else:
            pixels1.fill((0, 0, 0))
            print('Off')

        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url

    def _run_flashing(self):
        for _ in range(3):  # Flash three times
            pixels1.fill((0, 220, 0))
            time.sleep(3)
            pixels1.fill((220, 0, 0))
            time.sleep(3)
            pixels1.fill((0, 0, 220))
            time.sleep(3)
        pixels1.fill((0, 0, 0))  # Turn off after flashing

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
