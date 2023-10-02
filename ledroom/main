from serial_com import SerialCommunication
from strip import Strip
from controller import ProgramController
import board
import serial 

port = '/dev/ttyUSB0'  # Change this to the correct serial port for your device
baud_rate = 9600  #baud rate of communication 

ser = serial.Serial(port, baud_rate, timeout = 3) #serial object raspberry pi will use

strip1 = Strip(board.D21,300,0.05) #creates instance of strip
model = SerialCommunication(strip1,ser) #creates serial com instance (model) with serial and strip instance
controller = ProgramController(model,strip1) #creates controller instance with instane of serial com and strip 
controller.run_program() #runs program
 
