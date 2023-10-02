// #include <Arduino.h>
#include <LiquidCrystal.h> //LCD Screen library

// Global Variable Instantiation
// Pins
LiquidCrystal lcd(7, 6, 5, 4, 3, 2); // LCD screen pins
#define buttPin 8
#define potPin1 A0
#define potPin2 A1

// Variables
int pattIndex = -1; // invalid indexes to force an update on the first loop
int colorIndex = -1;
int colorsNeeded = -1;
int selectedColorCount = -1;
static int lastSentBrightness = -1;
bool userFinished = false;                  // used for readability in the main loop to indicate if the user has finished selecting colors
bool sendBrightnessFlag = false;            // only send brightness once per change
unsigned long lastBrightnessChangeTime = 0; // Time when the brightness was last changed. Unsigned longs are often used for "time" variables as they are long and can't be negative
const unsigned long brightnessDisplayDuration = 2500;
String patternName;
String colorName1;
String colorName2;
String colorName3;
String colorName4;

// LED patterns and amount of colors needed for each pattern
const char patterns[][20] PROGMEM = { // array of pointers to strings meaning each element of the array is a pointer to a string. PROGMEM stores the strings in flash memory instead of SRAM to save memory
    "Off", "Transition", "Flow", "Twinkle", "Fill Color",
    "Dual Catapillars", "Rainbow", "Pulse", "Sin Wave", "Shooting Stars", "Bouncing Ball", "Shimmer", "Fire"};

const char sendPatternNames[][20] PROGMEM = { // Pattern names sent to the Serial Monitor formatted for the Raspberry Pi to read
    "Clear_Strip", "Transition_Effect", "Flow_Effect", "Twinkle_Effect", "Fill_Color_Effect",
    "Dual_Catapillars", "Rainbow", "Pulse", "Sin_Wave", "Shooting_Stars", "Bouncing_Ball", "Shimmer", "Fire"};

const byte colorCounts[] = { // array of bytes. Used bytes for small numbers to save memory
    0, // Off
    0, // Transition
    2, // Flow
    4, // Twinkle
    1, // Fill Color
    4, // Dual Catapillars
    0, // Rainbow
    3, // Pulse
    4, // Sin Wave
    1, // Shooting Stars
    1, // Bouncing Ball
    1, // Shimmer
    1  // Fire
};

// Color names 
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

const char sendColorNames[][20] PROGMEM = { // Color names sent to the Serial Monitor formatted for the Raspberry Pi to read
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
 
class ArduinoUserDis // Class handles all user display functions and variables
{
public:
    int brightness; 

    bool isButtonPressed() // Function accounts for button press debouncing and button hold
    {
        static bool buttonWasPressed = false; // Static variables are only initialized once and keep their values between function calls
        static bool buttonState = false;      // These two variables are to account for if the button is pressed between function calls (debouncing/button hold)
        int currentButtonState = digitalRead(buttPin); 

        if (currentButtonState != buttonState) // Returns true when the button is pressed, false at any other time
        {
            buttonState = currentButtonState; 
            if (currentButtonState == HIGH)   // Button was released, reset the buttonWasPressed variable so the button can be pressed again
            {
                buttonWasPressed = false;
            }
            else // Button was pressed
            {
                if (!buttonWasPressed) // If the button was not already pressed, return true. Accounts for button hold
                {
                    buttonWasPressed = true;
                    return true; 
                }
            }
        }

        return false; // return false if the button was already pressed (debouncing/hold) or if the button was not pressed
    }

    void brightDis() // Function displays the brightness screen
    {
        int potVal = analogRead(potPin1);
        
        lcd.setCursor(3, 0);
        lcd.print("Brightness");
        brightness = map(potVal, 0, 1023, 0, 100); // Map the potentiometer value 0-1023 to brightness 0-100
        // Center the text in the second line (16 characters wide LCD), printing a space to overwrite the previous value and keep the numbers aligned
        if (brightness < 10)                       
        {
            lcd.setCursor(8, 1);
            lcd.print("  ");
        }
        else if (brightness < 100) 
        {
            lcd.setCursor(9, 1);
            lcd.print(" ");
        }
        lcd.setCursor(7, 1);
        lcd.print(brightness);
    }

    void pattDis(int newPotVal) // Function displays the pattern screen. The newPotVal parameter is the current potentiometer value
    {
        int newPattIndex = map(newPotVal, 0, 1023, 0, sizeof(patterns) / sizeof(patterns[0]) - 1); // Map the potentiometer value 0-1023 to pattern index 0-15 (16 patterns). Math so if more patterns are added the code doesn't need to be changed

        // Only update the display if the pattern has changed to prevent flickering.
        if (newPattIndex != pattIndex) // First time through this will always be true because pattIndex is initialized to -1
        {
            pattIndex = newPattIndex; 
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

    void colorDis(int newPotVal, int colorsNeeded) // Function displays the color screen. The colorsNeeded parameter is used to determine how many colors the user needs to select for the current pattern
    {
        int newColorIndex = map(newPotVal, 0, 1023, 0, sizeof(colorNames) / sizeof(colorNames[0]) - 1); // Map the potentiometer value 0-1023 to color index 0-99 (100 colors)

        // Only update the display if the color has changed to prevent flickering.
        if (newColorIndex != colorIndex) 
        {
            colorIndex = newColorIndex; 
            lcd.clear();
        }
        lcd.setCursor(0, 0);
        lcd.print(F("Choose Color "));
        lcd.print(selectedColorCount + 1);
        lcd.print("/");
        lcd.print(colorCounts[pattIndex]); // Display the total color count required for the pattern

        // Center the text in the second line (16 characters wide LCD)
        int colorLength = strlen_P(colorNames[newColorIndex]);
        int padding = (16 - colorLength) / 2;
        lcd.setCursor(padding, 1);
        lcd.print(reinterpret_cast<const __FlashStringHelper *>(colorNames[newColorIndex]));
    }
};

class UserData // Class handles all user input data and variables which are sent to the Raspberry Pi via the Serial Monitor
{
public:
    // Variables containing the data to be sent to the Raspberry Pi which needs string variables
    String brightnessSend;
    String patternSend; 
    String colorSend1;
    String colorSend2;
    String colorSend3;
    String colorSend4;

    void updateData(String newBrightness, String patternName, String colorName1, String colorName2, String colorName3, String colorName4) // Function updates the data to be sent to the Raspberry Pi
    {
        brightnessSend = newBrightness;
        patternSend = patternName;
        colorSend1 = colorName1;
        colorSend2 = colorName2;
        colorSend3 = colorName3;
        colorSend4 = colorName4;
    }

    void sendPattern() // Function sends the pattern and its colors to the Raspberry Pi via the Serial Monitor
    {
        Serial.print(F("Pattern ")); // Raspberry Pi will look for this string to know when to read the pattern and color names
        Serial.print(patternSend); 
        Serial.print(F(" "));
        Serial.print(colorSend1); 
        Serial.print(F(" "));
        Serial.print(colorSend2); 
        Serial.print(F(" "));
        Serial.print(colorSend3); 
        Serial.print(F(" "));
        Serial.println(colorSend4); 
    }

    void sendBright() // Function sends the brightness to the Rasberry Pi via the Serial Monitor
    {
        Serial.print(F("Brightness "));
        Serial.println(brightnessSend); 
    }
};

// Declare instances of the classes
ArduinoUserDis myUserDis; 
UserData myUserData;      

enum State // Enumeration for readability in the main loop to indicate the current state
{
    OFF,
    PATTERN,
    COLOR
};

State currentState = OFF; // Initialize the current state to OFF

void setup()
{
    pinMode(buttPin, INPUT_PULLUP); 
    lcd.begin(16, 2); // Initialize the LCD screen with 16 columns and 2 rows
    Serial.begin(9600); 
}

void loop()
{
    int potVal1 = analogRead(potPin1);
    int brightness = map(potVal1, 0, 1023, 0, 100);
    static int lastBrightness = -1;
    float brightConvert; // Used to convert brightness to a float
    String brightnessString;

    switch (currentState)
    {
    case OFF: // Runs when the user is not selecting patterns or colors and the LCD screen is off
        if (myUserDis.isButtonPressed()) // If the button is pressed, change the state to PATTERN and start the user input process
        {
            lcd.clear();
            currentState = PATTERN;
            delay(200); // debounce
        }

        if (abs(brightness - myUserDis.brightness) > 2) // accounts for slight voltage variation in the potentiometer and will update lastBrightnessChangeTime if the brightness changes
        {
            lastBrightnessChangeTime = millis(); // Update the last change time
            myUserDis.brightness = brightness;
        }
        if (millis() - lastBrightnessChangeTime < brightnessDisplayDuration) // If the time since the last brightness change is less than the brightness display duration
        {
            myUserDis.brightDis(); 
            sendBrightnessFlag = true; 
        }
        else if (brightness != lastBrightness) 
        {
            lcd.clear();
            if (abs(brightness - lastSentBrightness) > 2 && sendBrightnessFlag) // If the brightness changed more than 2 and it has not been sent since the last change
            {
                lastBrightness = brightness;
                brightConvert = map(brightness, 0, 100, 0, 500) / 10000.; // Converts the 0-100 brightness to a float 0-0.05
                brightnessString = String(brightConvert, 3);
                myUserData.updateData(brightnessString, patternName, colorName1, colorName2, colorName3, colorName4);
                lcd.clear();
                myUserData.sendBright();
                lastSentBrightness = brightness;
                sendBrightnessFlag = false; // Reset the sendBrightnessFlag so the brightness can be sent again
            }
        }
        else
        {
            lcd.clear();
        }
        break;

    case PATTERN: // Runs when the user is selecting a pattern
        myUserDis.pattDis(analogRead(potPin2)); 
        if (myUserDis.isButtonPressed())
        {
            patternName = reinterpret_cast<const __FlashStringHelper *>(sendPatternNames[pattIndex]); // Get the pattern name string
            selectedColorCount = 0; // Reset the selected color count for the new pattern in the next state
            currentState = COLOR;
            delay(200); // Debounce
            lcd.clear();
        }
        break;

    case COLOR: // Runs when the user is selecting colors
        if (selectedColorCount >= colorCounts[pattIndex]) // If all colors for the pattern are selected, turn off the program and send the data to the Raspberry Pi
        {
            // Resets unused colorName variables to "NA" if the user did not select all 4 colors
            if (selectedColorCount >= 0 && selectedColorCount <= 3)
            {
                for (int i = selectedColorCount; i < 4; i++)
                {
                    switch (i)
                    {
                    case 0:
                        colorName1 = "NA";
                        break;
                    case 1:
                        colorName2 = "NA";
                        break;
                    case 2:
                        colorName3 = "NA";
                        break;
                    case 3:
                        colorName4 = "NA";
                        break;
                    }
                }
            }
            // Send the pattern data to the Raspberry Pi
            myUserData.updateData(brightnessString, patternName, colorName1, colorName2, colorName3, colorName4);
            myUserData.sendPattern();

            userFinished = true;
            currentState = OFF;
            lcd.clear();
            lcd.setCursor(4, 0);
            lcd.print("Request");
            lcd.setCursor(6, 1);
            lcd.print("Sent");
            delay(2000);
            lcd.clear();
        }
        else
        {
            myUserDis.colorDis(analogRead(potPin2), colorCounts[pattIndex]);
        }
        if (myUserDis.isButtonPressed()) // If the button is pressed, select the color and update the LCD screen
        {
            colorIndex = map(analogRead(potPin2), 0, 1023, 0, sizeof(colorNames) / sizeof(colorNames[0]) - 1); // Map the potentiometer value 0-1023 to color index 0-99 (100 colors)

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

            selectedColorCount++; // Increment selected color count to keep track of how many colors have been selected

            lcd.setCursor(0, 0);
            lcd.print("Color Selected! ");
            delay(800); 
        }
        break;
    }
}