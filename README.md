# LEDRoom
This is the code for a personal project I am undergoing for my common room with my roomate Logan Schneider. The project consists of an arduino uno connected to several potentiometers allowing the user to input desired patterns and colors. This data is then communicated to a raspberry pi 4b via USB serial bus, which then displays the desired inputs on a WS2812B strip.

The strip class consists of all the effects I have programmed using the neopixel library. Many of the workings of these effects take artistic or programming inspiration from the FASTLed library. 

The SerialCom class is the raspberry pi end of the communication with the raspberry pi, while the 
