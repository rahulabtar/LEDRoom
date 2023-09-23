import serial
import time
from strip import Strip
import board

# ['flow', 'Red, 'Green', 'NA', 'NA', '0.125']
# Define the serial port and baud rate
port = '/dev/ttyUSB0'  # Change this to the correct serial port for your device
baud_rate = 9600 
print("started!")

class SerialCommunication:
    def __init__(self):
        pass
    def translate_request(self,request):
        request = request.split()
        request[5] = float(request[5])
        return request
    def request_recieved(self):
        serial.write('Request Recieved!')
    

Com1 = SerialCommunication()
print(Com1.translate_request('flow Red Green NA NA 0.125'))

