#include <Wire.h>
#include <SoftwareSerial.h>
#include "MAX30100_PulseOximeter.h"
 
#include "Wire.h"
#include "Adafruit_GFX.h"
#include "OakOLED.h"

#define REPORTING_PERIOD_MS 1000

SoftwareSerial bluetoothModule(2, 3); // RX, TX
OakOLED oled; 
PulseOximeter pox;
 
uint32_t tsLastReport = 0;
float cholVoltage = 0;
float chol = 0;
float bpm = 0;
int spo2 = 0;
 
void setup()
{
  Serial.begin(9600);
  bluetoothModule.begin(9600); 

  oled.begin();
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(1);
  oled.setCursor(0, 0);
   
  oled.println("Initializing pulse oximeter..");
  oled.display();
  Serial.print("Initializing pulse oximeter..");
   
  if (!pox.begin()) {
    Serial.println("FAILED");
    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0, 0);
    oled.println("FAILED");
    oled.display();
    for(;;);
  } else {
    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0, 0);
    oled.println("SUCCESS");
    oled.display();
    Serial.println("SUCCESS");
  }
}
 
void loop()
{
  analogWrite(9, 255);
  pox.update();
   
  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
    cholVoltage = analogRead(A0) * (5 / 1023.0);
    chol = (355.87*(cholVoltage+1.78))-591.46;
    bpm = pox.getHeartRate();
    spo2 = pox.getSpO2();

    Serial.print("Heart BPM:");
    Serial.print(pox.getHeartRate());
    Serial.print("-----");
    Serial.print("Oxygen Percent:");
    Serial.print(pox.getSpO2());
    Serial.println("\n");   

    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0,16);
    oled.println(bpm);
     
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0, 0);
    oled.println("Heart BPM");
     
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0, 30);
    oled.println("Spo2");
     
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(0,45);
    oled.println(spo2);

    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(45, 16);
    oled.println("Chol");
   
    oled.setTextSize(1);
    oled.setTextColor(1);
    oled.setCursor(45, 30);
    oled.println(chol);
    oled.display();

    Serial.println(bluetoothModule.available());
    if(bluetoothModule.available()) {
      bluetoothModule.write(chol);
      bluetoothModule.write(bpm);
    }

    tsLastReport = millis();
  }
}