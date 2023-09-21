import serial
import time
from strip import Strip
import board
# Define the serial port and baud rate
port = '/dev/ttyUSB0'  # Change this to the correct serial port for your device
baud_rate = 9600
print("started!")
stripex = Strip(board.D21,50,0.05)

try:
    print("Got here")
    # Open the serial connection
    ser = serial.Serial(port, baud_rate, timeout = 3)

    print("here too")
    # Read and print data from the serial port
    while True:
        print("data:")
        #time.sleep(1000)
        data = ser.readline().decode('utf-8').strip()
        print(data)
        if data == 'on':
            stripex.fill_color_effect()
        elif data == 'off':
            stripex.clear_strip()

except serial.SerialException as e:
    print(f"Serial Port Error: {e}")
except KeyboardInterrupt:
    # Close the serial connection when Ctrl+C is pressed
    ser.close()
