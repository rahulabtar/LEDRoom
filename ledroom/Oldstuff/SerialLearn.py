import serial
import time
import board
# Define the serial port and baud rate
port = '/dev/ttyUSB0'  # Change this to the correct serial port for your device
baud_rate = 9600
print("started!")

# pattern color1 color2 color3 color4 brightness
# flow Red Green None None 0.24
#.split()
# ['flow', 'Red, 'Green', 'NA', 'NA', '0.125']

try:
    print("Got here")
    # Open the serial connection
    ser = serial.Serial(port, baud_rate)

    print("here too")
    # Read and print data from the serial port
    while True:
        #time.sleep(1000)
        data = ser.readline().decode('utf-8').strip()
        if 'e' in data:
            print("data:")
            print(data)

except serial.SerialException as e:
    print(f"Serial Port Error: {e}")
except KeyboardInterrupt:
    # Close the serial connection when Ctrl+C is pressed
    ser.close()
