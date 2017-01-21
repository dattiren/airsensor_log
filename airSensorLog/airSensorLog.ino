#include "DHT.h"
#include <stdio.h>

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
float hcho_R0 = 30.0;
float hcho_ppm = 0;
float value_adj = 49;

DHT dht(DHTPIN, DHTTYPE);

void setup(){
  Serial.begin(9600);
  dht.begin();
}
 
void loop() {
  //hcho, mq135, h, t
  //HCHO sensor
  hcho_value = analogRead(A1);
  //float vol = hcho_value * 4.95/1023;
  float hcho_Rs = (1023.0/hcho_value)-1;
  hcho_ppm = pow(10.0,((log10(hcho_Rs/hcho_R0)-0.0827)/(-0.4807)));
  char hcho[12];
  dtostrf(hcho_ppm,3,2,hcho);
//  Serial.print(hcho_Rs);
//  Serial.print(",");

  //Mq135 sensor
  mq135_value = analogRead(A0);
  mq135_value = mq135_value + value_adj;
//  Serial.print(mq135_value, DEC);
//  Serial.print(",");
  char mq135[12];
  dtostrf(mq135_value,3,2,mq135);

  

  //humidity & tempareture sensor
  h = dht.readHumidity();
  t = dht.readTemperature();
  f = dht.readTemperature(true);
//  float hif = dht.computeHeatIndex(f, h);
//  float hic = dht.computeHeatIndex(t, h, false);
  char temp[12];
  dtostrf(t,3,2,temp);
  char humi[12];
  dtostrf(h,3,2,humi);

//  Serial.print(",");
//  Serial.print(h);
//  Serial.print(",");
//  Serial.println(t);
 
  char buf[44];
  sprintf(buf, "%s,%s,%s,%s", hcho, mq135, humi, temp);
  Serial.println(buf);
  
  delay(1000);
}

