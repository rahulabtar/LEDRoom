import serial
import time
import board
from strip import Strip

# ['flow', 'Red, 'Green', 'NA', 'NA', '0.125']


class SerialCommunication:
    def __init__(self,strip1,ser):
        self.strip1 = strip1
        self.ser = ser
    def get_request(self):
        data = ser.readline().decode('utf-8').strip()
        return data
    def translate_request(self,request):
        """ This method takes in a request (Serial String) in the form of a string and converts it into a list with a string representing the patterm, 4 color values as RGB Decimal tuples or "NA", and a float representing brightness"""
        request = request.split()
        request[1] = self.strip1.COLOR_DICT[str(request[1])]
        request[2] = self.strip1.COLOR_DICT[str(request[2])]
        request[3] = self.strip1.COLOR_DICT[str(request[3])]
        request[4] = self.strip1.COLOR_DICT[str(request[4])]
        request[5] = float(request[5])
        return request
    def request_recieved(self):
        serial.write('Request_Recieved')
    
stripex = Strip(board.D21,300,0.05)
Com1 = SerialCommunication(stripex)


