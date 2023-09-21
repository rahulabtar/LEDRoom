# 1 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
void setup() {
  Serial.begin(9600);
  // Initialize the built-in LED (pin 13) as an output
  pinMode(13, 0x1);
}

void loop() {
  // Turn the LED on
  digitalWrite(13, 0x1);
  delay(1000); // Wait for 1 second (1000 milliseconds)
  Serial.println("on");

  // Turn the LED off
  digitalWrite(13, 0x0);
  delay(1000); // Wait for 1 second (1000 milliseconds)
  Serial.println("off");
}
