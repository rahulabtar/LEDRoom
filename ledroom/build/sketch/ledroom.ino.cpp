#include <Arduino.h>
#line 1 "/home/rahul/LEDRoom/ledroom/ledroom.ino"
//#include <Arduino.h>
#include <LiquidCrystal.h> //LCD Screen library

// class string of
// string concatination, Send data so everything is separated by a space.
// CLass to get data, Class to send data. Data send = String of data with order,
// pattern color color color brightness (float 0-1)
// Make sure send pattern color1 color2 color3 color4 brightness. Send NA if no color.

// Have request timeout / request recieved if it works.

// Global Variable Instantiation
// Pins
LiquidCrystal lcd(7, 6, 5, 4, 3, 2); // LCD screen pins
#define buttPin 8
#define potPin1 A0
#define potPin2 A1

// Variables
bool isRunning = false;                               // flag to indicate if the program is running.
int pattIndex = -1;                                   // invalid index to force initial update
int colorIndex = -1;                                  // invalid index to force initial update
int colorsNeeded = 0;                                 // invalid index to force initial update
int selectedColorCount = 0;                           // invalid index to force initial update
bool userFinished = false;                            // flag to indicate if the user has finished selecting colors
unsigned long lastBrightnessChangeTime = 0;           // Time when the brightness was last changed. Unsigned longs are often used for "time" variables as they are long and can't be negative
const unsigned long brightnessDisplayDuration = 5000; // Display brightness screen for 5 seconds after the last potentiometer change
String patternName;
String colorName1;
String colorName2;
String colorName3;
String colorName4;

// LED patterns and amount of colors needed for each pattern
const char patterns[][20] PROGMEM = { // array of pointers to strings meaning each element of the array is a pointer to a string. This is useful to save memory and is a common way to store strings in C/C++
    "Clear Strip", "TransitionEffect", "Flow Effect", "Twinkle Effect", "Fill Color Effect",
    "Dual Catapillars", "Rainbow", "Pulse", "Sin Wave", "Shooting Stars", "Bouncing Ball", "Shimmer", "Fire"};

const char sendPatternNames[][20] PROGMEM = { // array of pointers to strings meaning each element of the array is a pointer to a string. This is useful to save memory and is a common way to store strings in C/C++
    "Clear_Strip", "Transition_Effect", "Flow_Effect", "Twinkle_Effect", "Fill_Color_Effect",
    "Dual_Catapillars", "Rainbow", "Pulse", "Sin_Wave", "Shooting_Stars", "Bouncing_Ball", "Shimmer", "Fire"};

const byte colorCounts[] = {
    // array of bytes. Used bytes for small numbers to save memory
    0, // Clear Strip
    0, // Transition Effectd
    2, // Flow Effect
    4, // Twinkle Effect
    1, // Fill Color Effect
    4, // Dual Catapillars
    0, // Rainbow
    3, // Pulse
    3, // Sin Wave
    1, // Shooting Stars
    1, // Bouncing Ball
    4, // Shimmer
    1  // Fire
};

// Color names and RGB values for each color
const char colorNames[][20] PROGMEM = {
    "Black", "Maroon", "Dark Red", "Brown", "Firebrick", "Crimson", "Red", "Tomato", "Coral", "Indian Red", "Light Coral", "Dark Salmon",
    "Salmon", "Light Salmon", "Orange Red", "Dark Orange", "Orange", "Gold", "Dark Golden Rod", "Golden Rod", "Pale Golden Rod", "Dark Khaki", "Khaki",
    "Olive", "Yellow", "Yellow Green", "Dark Olive Green", "Olive Drab", "Lawn Green", "Chartreuse", "Green Yellow", "Dark Green", "Green",
    "Forest Green", "Lime", "Lime Green", "Light Green", "Pale Green", "Dark Sea Green", "Medium Spring Green", "Spring Green",
    "Sea Green", "Medium Aqua Marine", "Medium Sea Green", "Light Sea Green", "Dark Slate Gray", "Teal", "Dark Cyan", "Aqua",
    "Cyan", "Light Cyan", "Dark Turquoise", "Turquoise", "Medium Turquoise", "Pale Turquoise", "Aqua Marine", "Powder Blue",
    "Cadet Blue", "Steel Blue", "Corn Flower Blue", "Deep Sky Blue", "Dodger Blue", "Light Blue", "Sky Blue", "Light Sky Blue",
    "Midnight Blue", "Navy", "Dark Blue", "Medium Blue", "Blue", "Royal Blue", "Blue Violet", "Indigo",
    "Dark Slate Blue", "Slate Blue", "Medium Slate Blue", "Medium Purple", "Dark Magenta", "Dark Violet", "Dark Orchid", "Medium Orchid",
    "Thistle", "Plum", "Violet", "Orchid", "Medium Violet Red", "Pale Violet Red", "Deep Pink", "Hot Pink", "White"};

// Color names and RGB values for each color
const char sendColorNames[][20] PROGMEM = {
    "Black", "Maroon", "Dark_Red", "Brown", "Firebrick", "Crimson", "Red", "Tomato", "Coral", "Indian_Red", "Light_Coral", "Dark_Salmon",
    "Salmon", "Light_Salmon", "Orange_Red", "Dark_Orange", "Orange", "Gold", "Dark_Golden_Rod", "Golden_Rod", "Pale_Golden_Rod", "Dark_Khaki", "Khaki",
    "Olive", "Yellow", "Yellow_Green", "Dark_Olive_Green", "Olive_Drab", "Lawn_Green", "Chartreuse", "Green_Yellow", "Dark_Green", "Green",
    "Forest_Green", "Lime", "Lime_Green", "Light_Green", "Pale_Green", "Dark_Sea_Green", "Medium_Spring_Green", "Spring_Green",
    "Sea_Green", "Medium_Aqua_Marine", "Medium_Sea_Green", "Light_Sea_Green", "Dark_Slate_Gray", "Teal", "Dark_Cyan", "Aqua",
    "Cyan", "Light_Cyan", "Dark_Turquoise", "Turquoise", "Medium_Turquoise", "Pale_Turquoise", "Aqua_Marine", "Powder_Blue",
    "Cadet_Blue", "Steel_Blue", "Corn_Flower_Blue", "Deep_Sky_Blue", "Dodger_Blue", "Light_Blue", "Sky_Blue", "Light_Sky_Blue",
    "Midnight_Blue", "Navy", "Dark_Blue", "Medium_Blue", "Blue", "Royal_Blue", "Blue_Violet", "Indigo",
    "Dark_Slate_Blue", "Slate_Blue", "Medium_Slate_Blue", "Medium_Purple", "Dark_Magenta", "Dark_Violet", "Dark_Orchid", "Medium_Orchid",
    "Thistle", "Plum", "Violet", "Orchid", "Medium_Violet_Red", "Pale_Violet_Red", "Deep_Pink", "Hot_Pink", "White"};

class ArduinoUserDis
{
public:
    int brightness; // Brightness of the LED strip

    bool isButtonPressed() // Function to check if the button is pressed which accounts for debouncing and button hold
    {
        static bool buttonWasPressed = false; // Static variables are only initialized once and keep their values between function calls
        static bool buttonState = false;      // these two variables are to account for if the button is pressed between function calls (debouncing/button hold)
        int currentButtonState = digitalRead(buttPin);

        if (currentButtonState != buttonState) // If the button state has changed, was it pressed, was it released
        {
            buttonState = currentButtonState; // Update the button state
            if (currentButtonState == HIGH)   // Button was released
            {
                buttonWasPressed = false;
            }
            else // Button was pressed
            {
                if (!buttonWasPressed)
                {
                    buttonWasPressed = true;
                    return true; // return true when the button is pressed
                }
            }
        }

        return false; // return false if the button was already pressed (debouncing/hold) or if the button was not pressed
    }

    void brightDis() // Function to display the brightness on the LCD screen
    {
        lcd.setCursor(3, 0);
        lcd.print("Brightness");
        int potVal = analogRead(potPin1);
        brightness = map(potVal, 0, 1023, 0, 100); // Map the potentiometer value 0-1023 to brightness 0-100
        if (brightness < 10)                       // If the brightness is less than 10, print an extra space to keep the numbers aligned
        {
            lcd.setCursor(8, 1);
            lcd.print("  ");
        }
        else if (brightness < 100) // If the brightness is less than 100, print an extra space to keep the numbers aligned
        {
            lcd.setCursor(9, 1);
            lcd.print(" ");
        }
        lcd.setCursor(7, 1);
        lcd.print(brightness);
    }

    void pattDis(int newPotVal)
    {
        int newPattIndex = map(newPotVal, 0, 1023, 0, sizeof(patterns) / sizeof(patterns[0]) - 1); // Map the potentiometer value 0-1023 to pattern index 0-15 (16 patterns). Math so if more patterns are added the code doesn't need to be changed

        // Only update the display if the pattern has changed to prevent flickering.
        if (newPattIndex != pattIndex) // First time through this will always be true because pattIndex is initialized to -1
        {
            pattIndex = newPattIndex; // Update the pattern index
            lcd.clear();
        }
        lcd.setCursor(4, 0);
        lcd.print(F("Pattern"));

        // Center the text in the second line (16 characters wide LCD)
        int patternLength = strlen_P(patterns[newPattIndex]);
        int padding = (16 - patternLength) / 2;

        lcd.setCursor(padding, 1);
        lcd.print(reinterpret_cast<const __FlashStringHelper *>(patterns[newPattIndex]));
    }

    void colorDis(int newPotVal, int colorsNeeded)
    {
        int newColorIndex = map(newPotVal, 0, 1023, 0, sizeof(colorNames) / sizeof(colorNames[0]) - 1); // Map the potentiometer value 0-1023 to color index 0-99 (100 colors). Math so if more colors are added the code doesn't need to be changed

        // Only update the display if the color has changed to prevent flickering.
        if (newColorIndex != colorIndex) // First time through this will always be true because colorIndex is initialized to -1
        {
            colorIndex = newColorIndex; // Update the color index
            lcd.clear();
        }
        lcd.setCursor(0, 0);
        lcd.print(F("Choose Color "));
        lcd.print(selectedColorCount + 1); // Display the selected color count
        lcd.print("/");
        lcd.print(colorCounts[pattIndex]); // Display the total color count for the pattern

        // Center the text in the second line (16 characters wide LCD)
        int colorLength = strlen_P(colorNames[newColorIndex]);
        int padding = (16 - colorLength) / 2;

        lcd.setCursor(padding, 1);
        lcd.print(reinterpret_cast<const __FlashStringHelper *>(colorNames[newColorIndex]));
    }
};

class UserData
{
public:
    String brightnessSend;
    String patternSend; // Change the data type to String
    String colorSend1;
    String colorSend2;
    String colorSend3;
    String colorSend4;

    void updateData(String newBrightness, String patternName, String colorName1, String colorName2, String colorName3, String colorName4)
    {
        brightnessSend = newBrightness;
        patternSend = patternName;
        colorSend1 = colorName1;
        colorSend2 = colorName2;
        colorSend3 = colorName3;
        colorSend4 = colorName4;
    }

    void printUserData()
    {
        Serial.print(F("Pattern "));
        Serial.print(patternSend); // Print the pattern name
        Serial.print(F(" "));
        Serial.print(colorSend1); // Print the first color name
        Serial.print(F(" "));
        Serial.print(colorSend2); // Print the second color name
        Serial.print(F(" "));
        Serial.print(colorSend3); // Print the third color name
        Serial.print(F(" "));
        Serial.println(colorSend4); // Print the fourth color name
    }

    void printBright()
    {
        Serial.print(F("Brightness "));

        Serial.println(brightnessSend); // Print the brightness
    }
};

ArduinoUserDis myUserDis; // Declare an instance of the LEDStrip class
UserData myUserData;      // Declare an instance of the UserData class

enum State // Enumeration to keep track of the current state of the program
{
    OFF,
    PATTERN,
    COLOR
};

State currentState = OFF; // Initialize the current state to OFF

void setup()
{
    pinMode(buttPin, INPUT_PULLUP);
    lcd.begin(16, 2);
    Serial.begin(9600); // Initialize serial communication at 9600 baud
}

void loop()
{
    int potVal1 = analogRead(potPin1);
    int brightness = map(potVal1, 0, 1023, 0, 100);
    float bright01;

    static int lastBrightness = -1;

    switch (currentState)
    {
    case OFF:
        if (abs(brightness - myUserDis.brightness) > 5)
        {
            lastBrightnessChangeTime = millis(); // Update the last change time
            myUserDis.brightness = brightness;
        }
        if (myUserDis.isButtonPressed())
        {
            lcd.clear();
            currentState = PATTERN;
            delay(200); // debounce
        }

        if (millis() - lastBrightnessChangeTime < brightnessDisplayDuration) // If the time since the last brightness change is less than the brightness display duration
        {
            myUserDis.brightDis(); // Display brightness screen for 3 seconds after the last potentiometer change
        }
        else if (brightness != lastBrightness)
        {
            // Only send data when brightness changes
            lastBrightness = brightness;
            UserData userData;
            bright01 = map(brightness, 0, 100, 0, 500) / 10000.0;
            String brightnessString = String(bright01, 4);
            userData.updateData(brightnessString, patternName, colorName1, colorName2, colorName3, colorName4);
            lcd.setCursor(0, 0);
            lcd.print("Bright changed!");
            delay(2000);
            lcd.clear();
            userData.printBright();
        }
        else
        {
            lcd.clear();
        }
        break;

    case PATTERN:
        myUserDis.pattDis(analogRead(potPin2));
        if (myUserDis.isButtonPressed())
        {
            //  Get string variable of pattern name
            patternName = reinterpret_cast<const __FlashStringHelper *>(sendPatternNames[pattIndex]);
            selectedColorCount = 0; // Reset the selected color count for the new pattern in the next state
            currentState = COLOR;
            delay(200); // Debounce
        }
        break;

    case COLOR:
        // If all colors are selected, turn off the program
        if (selectedColorCount >= colorCounts[pattIndex])
        {
            userFinished = true;
            currentState = OFF;
            lcd.clear();
            lcd.setCursor(4, 0);
            lcd.print("Sending");
            lcd.setCursor(3, 1);
            lcd.print("Request...");

            if (selectedColorCount == 0)
            {
                colorName1 = "NA";
                colorName2 = "NA";
                colorName3 = "NA";
                colorName4 = "NA";
            }
            else if (selectedColorCount == 1)
            {
                colorName2 = "NA";
                colorName3 = "NA";
                colorName4 = "NA";
            }
            else if (selectedColorCount == 2)
            {
                colorName3 = "NA";
                colorName4 = "NA";
            }
            else if (selectedColorCount == 3)
            {
                colorName4 = "NA";
            }

            // Create an instance of UserData, update it, and print the data
            UserData userData;
            brightness = map(potVal1, 0, 1023, 0, 100);
            bright01 = brightness / 100.;
            String brightnessString = String(bright01);

            userData.updateData(brightnessString, patternName, colorName1, colorName2, colorName3, colorName4);

            userData.printUserData();

            delay(5000);
            lcd.clear();
        }
        else
        {
            myUserDis.colorDis(analogRead(potPin2), colorCounts[pattIndex]);
        }
        if (myUserDis.isButtonPressed())
        {
            // get color selected string
            colorIndex = map(analogRead(potPin2), 0, 1023, 0, sizeof(colorNames) / sizeof(colorNames[0]) - 1); // Map the potentiometer value 0-1023 to color index 0-99 (100 colors). Math so if more colors are added the code doesn't need to be changed

            // Update the corresponding color name based on selectedColorCount
            if (selectedColorCount == 0)
            {
                colorName1 = reinterpret_cast<const __FlashStringHelper *>(sendColorNames[colorIndex]);
            }
            else if (selectedColorCount == 1)
            {
                colorName2 = reinterpret_cast<const __FlashStringHelper *>(sendColorNames[colorIndex]);
            }
            else if (selectedColorCount == 2)
            {
                colorName3 = reinterpret_cast<const __FlashStringHelper *>(sendColorNames[colorIndex]);
            }
            else if (selectedColorCount == 3)
            {
                colorName4 = reinterpret_cast<const __FlashStringHelper *>(sendColorNames[colorIndex]);
            }

            selectedColorCount++; // Increment selected color count

            lcd.setCursor(0, 0);
            lcd.print("Color Selected! ");
            delay(2000); // Display confirmation message for 2000 milliseconds
        }
        break;
    }

}
