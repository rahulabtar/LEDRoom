from Oldstuff.server import MyServer
from http.server import BaseHTTPRequestHandler, HTTPServer #allows server
from strip import Strip
import neopixel
import board


strip1 = Strip(board.D18,55,0.05)  
strip1.clear_strip()
server_address = ('10.69.0.114', 8000)
httpd = HTTPServer(server_address, lambda *args, **kwargs: MyServer(strip1, *args, **kwargs))
print('Server running at http://10.69.0.114:8000/')
httpd.serve_forever()


