import serial
import time
import board
from strip import Strip
import threading 

#This class is in charge of recieving and translating data sent to the rasberry pi from the arudino via USB serial bus

#All data from arduino comes in one of two forms; pattern data or brigtness data
#Patttern data holds information about a requested pattern from the arudino
#Has the form: Pattern, Pattern_Requested, Color1,Color2,Color3,Color4
#Ex:
#Pattern flow Red Green NA NA 
#If no color is given/needed for effect NA is sent
#Brightness data hold information about requested brightness change from the arudino for the strip
#Has the form: Brightness: float_number
#Ex:
#Brightness 0.04 
#On a scale from 0-0.05 to stop strip from taking too much power from raspberry pi


class SerialCommunication:
    def __init__(self,strip1,ser):
        self.strip1 = strip1
        self.ser = ser 
    def get_request(self): 
        """This method waits for a request from the arudino via serial moniter If one is recieved returns the data of the line from the serial moniter"""
        while True:
            data = self.ser.readline().decode('utf-8').strip()
            if 'e' in data:
                #print("data:")
                #print(data)
                return data
            #print("Serial Com Request Loop: Nothing Valuable Recieved Via Serial Moniter")
    def translate_request(self,request):
        """ This method takes in a request (Serial String) in the form of a string and converts it into a list with a string representing the patterm, 4 color values as RGB Decimal tuples or "NA", or a float representing brightness"""
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
        """This method writes back to the arduino verifying it recieved the request it sent. Will be implemented in future for easier debugging"""
        serial.write('Request_Recieved')






