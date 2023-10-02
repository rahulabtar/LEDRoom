import serial
import time
import board
from strip import Strip
import threading 
# ['flow', 'Red, 'Green', 'NA', 'NA', '0.125']


class SerialCommunication:
    def __init__(self,strip1,ser):
        self.strip1 = strip1
        self.ser = ser
    def get_request(self):
        while True:
            data = self.ser.readline().decode('utf-8').strip()
            if 'e' in data:
                #print("data:")
                #print(data)
                return data
            #print("Serial Com Request Loop: Nothing Valuable Recieved Via Serial Moniter")
    def translate_request(self,request):
        """ This method takes in a request (Serial String) in the form of a string and converts it into a list with a string representing the patterm, 4 color values as RGB Decimal tuples or "NA", and a float representing brightness"""
        request = request.split()
        if request[0] == 'Brightness':
            request[1] = float(request[1])
            return request
        if request[0] == 'Pattern':
            request[2] = self.strip1.COLOR_DICT[str(request[2])]
            request[3] = self.strip1.COLOR_DICT[str(request[3])]
            request[4] = self.strip1.COLOR_DICT[str(request[4])]
            request[5] = self.strip1.COLOR_DICT[str(request[5])]
            return request
    def request_recieved(self):
        serial.write('Request_Recieved')






