# LEDRoom
This is the code for a personal project my roomate Logan Schneider and I am undergoing for a led strip light in our common room.

The project consists of an arduino uno connected to several potentiometers allowing the user to input desired patterns and colors. This data is then communicated to a raspberry pi 4b via USB serial bus, which then displays the desired inputs on a WS2812B strip.

The strip class consists of all the effects I have programmed using the neopixel library. Many of the workings of these effects take artistic or programming inspiration from the FASTLed library. 

The SerialCom class is the raspberry pi end of the communication with the raspberry pi, while the controlelr class connects all these different classes together. (This is inspired by the Model View Controller method)

All the classes for the arduino are in the LEDRoom.ino file. 

The folder labeled "Old Stuff" contains prototype code for an HTTPs server user interface that we orginally planned to use and other code to help us learn and experiment. We decided to not use a web server interface due to dorm wifi security issues. 

Videos of the lights and controller in action soon!
