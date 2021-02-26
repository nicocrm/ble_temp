#include <Arduino_HTS221.h>
#include <ArduinoBLE.h>

#include "temp_service.h"

BLEService tempService(TEMP_SERVICE);
BLEFloatCharacteristic tempCharacteristic(TEMP_CHARACTERISTIC, BLERead | BLEBroadcast | BLENotify);

void setup() {
  Serial.begin(9600);
  // wait for serial to be ready
  while(!Serial);

   // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }
  
  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
  tempService.addCharacteristic(tempCharacteristic);
  BLE.addService(tempService);
  BLE.setAdvertisedService(tempService);
  BLE.setLocalName("TempBureau");
  tempCharacteristic.writeValue(-99.0);
  tempCharacteristic.broadcast();
  BLE.advertise();
}

void loop() { 
  float temperature = HTS.readTemperature();
  
  Serial.print("Temperature: ");
  Serial.println(temperature);
  tempCharacteristic.writeValue(temperature);
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());    
    Serial.print("RSSI: ");
    Serial.println(BLE.rssi());
  } else {
    Serial.println("No central");
  }
  delay(1000);
}
