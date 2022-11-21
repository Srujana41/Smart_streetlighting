#include <SPI.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

SoftwareSerial GPS_SoftSerial(4, 3);
TinyGPSPlus gps;

volatile float minutes, seconds;
volatile int degree, secs, mins;

int pir = 8;	
int led = 6;
int ldr = 7;
int ldr_value = 0; 

void setup() { 
  pinMode(ldr, INPUT);
  pinMode(led, OUTPUT);   
  pinMode(pir, INPUT);
  Serial.begin(9600);
  GPS_SoftSerial.begin(9600);
  while (!Serial);
  Serial.println("LoRa Sender & receiver");
 
  if (!LoRa.begin(434E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSyncWord(0xF3);
  LoRa.setTxPower(20);
}
 
void loop() 
{
  
  delay(1000);
  if(digitalRead(pir))
  {
    transmitter();
  }
  delay(1000);
  receiver();  
}


void transmitter()
{
    LoRa.beginPacket();
    LoRa.print("0003");
    LoRa.endPacket();    
  
}

void receiver()
{
  int packetSize = LoRa.parsePacket();
  if(packetSize == 5 )
  {
    Serial.print("packet received: ");
    while (LoRa.available()) {            // can't use readString() in callback, so
    Serial.print((char)LoRa.read());      // add bytes one by one
  }
  Serial.print("\n");
    delay(500);
    digitalWrite(led, HIGH);
    delay(1500);
    ldr_value = digitalRead(ldr);
    if (ldr_value == 1)
    {
      Serial.println("Fault detected");
      MyGPS();
     
    }
    delay(5000);
    digitalWrite(led, LOW);
  }
  
}


void MyGPS()
{
  
  smartDelay(1000);
  unsigned long start;
  double lat_val, lng_val, alt_m_val;
  bool loc_valid, alt_valid;
  lat_val = gps.location.lat(); 
  loc_valid = gps.location.isValid(); 
  lng_val = gps.location.lng();
  alt_m_val = gps.altitude.meters(); 
  alt_valid = gps.altitude.isValid(); 
    DegMinSec(lat_val);
    DegMinSec(lng_val); 

  if (!loc_valid)
  {
      LoRa.beginPacket();
      LoRa.print("3");
      LoRa.print(lat_val);
      LoRa.print(",");
      LoRa.print(lng_val);
      LoRa.endPacket();
      Serial.println("location not available");
  }
  else
  {
      Serial.print("lattitude value: ");
      Serial.println(lat_val);
      Serial.print("longitude value: ");
      Serial.print(lng_val);
      LoRa.beginPacket();
      LoRa.print("3");
      LoRa.print(lat_val);
      LoRa.print(",");
      LoRa.print(lng_val);
      LoRa.endPacket();
  }
}

void DegMinSec( double tot_val)
{
  degree = (int)tot_val;
  minutes = tot_val - degree;
  seconds = 60 * minutes;
  minutes = (int)seconds;
  mins = (int)minutes;
  seconds = seconds - minutes;
  seconds = 60 * seconds;
  secs = (int)seconds;
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do
  {
    while (GPS_SoftSerial.available()) 
    gps.encode(GPS_SoftSerial.read());
  } while (millis() - start < ms);
}


