from strip import strip
from View.server import MyServer
host_name = '10.69.0.114'  # IP Address of Raspberry Pi
host_port = 8000

http_server = HTTPServer((host_name, host_port), MyServer)

print("Server Starts - %s:%s" % (host_name, host_port))
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.server_close()

class led_controller:
    def __init__(self,strip,server):
        self.strip = strip
        self.server = server
    def run_program():
        while True:
            pass
