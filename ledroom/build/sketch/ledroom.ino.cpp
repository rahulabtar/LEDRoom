#include <Arduino.h>
#line 1 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
#line 1 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
void setup();
#line 7 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
void loop();
#line 1 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
void setup() {
  Serial.begin(9600);
  // Initialize the built-in LED (pin 13) as an output
  pinMode(13, OUTPUT);
}

void loop() {
  // Turn the LED on
  digitalWrite(13, HIGH);
  delay(1000); // Wait for 1 second (1000 milliseconds)
  Serial.println("on");

  // Turn the LED off
  digitalWrite(13, LOW);
  delay(1000); // Wait for 1 second (1000 milliseconds)
  Serial.println("off");
}

