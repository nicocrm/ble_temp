#include <Adafruit_Sensor.h>

#include <DHT_U.h>
#include <DHT.h>

//#include <Arduino_HTS221.h> 
#include <ArduinoBLE.h>


#define DHTPIN 2     // Digital pin connected to the DHT sensor 
#define DHTTYPE    DHT11     // DHT 11

#include "temp_service.h"

BLEService tempService(TEMP_SERVICE);
BLEFloatCharacteristic tempCharacteristic(TEMP_CHARACTERISTIC, BLERead | BLEBroadcast | BLENotify);


DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  // wait for serial to be ready
  while(!Serial);

   // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  dht.begin();
  tempService.addCharacteristic(tempCharacteristic);
  BLE.addService(tempService);
  BLE.setAdvertisedService(tempService);
  BLE.setLocalName("TempBureau");
  tempCharacteristic.writeValue(-99.0);
  tempCharacteristic.broadcast();
  BLE.advertise();
}

void loop() { 
  float temp = dht.readTemperature();
  if (isnan(temp)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(temp);
    Serial.println(F("°C"));
    tempCharacteristic.writeValue(temp);
  }  
  
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());    
    Serial.print("RSSI: ");
    Serial.println(BLE.rssi());  
  }
  delay(5000);
}
