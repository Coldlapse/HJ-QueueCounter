#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); 

unsigned long lastLcdResetTime = 0;
const unsigned long resetInterval = 300000; 

void setup() {
  Serial.begin(9600); 
  
  for (int pin = 6; pin <= 11; pin++) {
    pinMode(pin, INPUT);
  }

  initLCD();
}

void initLCD() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("System Ready...");
  delay(500);
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastLcdResetTime >= resetInterval) {
    initLCD();
    lastLcdResetTime = currentTime;
    Serial.println("LCD Re-initialized for stability.");
  }

  int n = 0; 
  for (int pin = 6; pin <= 11; pin++) {
    if (HIGH == digitalRead(pin)) {
      n++;
    }
  }

  lcd.clear();
  lcd.setCursor(0, 0); 
  lcd.print("IIDX LIGHTNING");

  lcd.setCursor(0, 1);
  lcd.print(n); 
  lcd.print(" Waiting");
  
  delay(400); 
}