#include <COS_MQ7.h>
#include "DHT.h"


// Pin definitions
#define ACTIVE_MONOX_PIN 5

#define READ_MONOX_PIN A3

//hum&temp sensor
#define DHTPIN 2  
#define DHTTYPE DHT22

// Variable initializations
int reading;
int mq135_value;
int hcho_value;
float h;
float t;
float f;
 
// Create CO sensor object
// Last parameter is the duration of initial purge in seconds,
// a negative value sets to purge to default: 500 seconds
COS_MQ7 MQ7(ACTIVE_MONOX_PIN, READ_MONOX_PIN, -1);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}
 
void loop() {
  //hcho, mq135, mq7, h, t, hic, hif
  //HCHO sensor
  hcho_value = analogRead(A1);
  float vol = hcho_value * 4.95/1023;
  Serial.print(vol);
  Serial.print(",");

  //Mq135 sensor
  mq135_value = analogRead(A0);
  Serial.print(mq135_value, DEC);
  Serial.print(",");

  //MQ7 sensor
  MQ7.Power_cycle();
  //for testing/info
  Serial.print(MQ7.Get_current_CO_reading());

  //humidity & tempareture sensor
  h = dht.readHumidity();
  t = dht.readTemperature();
  f = dht.readTemperature(true);
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.println(t);
  //Serial.print(", ");
  //Serial.print(hic);
  //Serial.print(", ");
  //Serial.println(hif);

  // wait a second (shouldn't be too much longer than 5-10 seconds)
  delay(1000);
}

