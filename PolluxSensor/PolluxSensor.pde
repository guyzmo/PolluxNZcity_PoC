// Powermeter shield 
// based on Enerduino 0.2 by Cesare Pizzi 
// http://enerduino.blogspot.com/2009/12/enerduino-english.html
// This Arduino application allow to monitor power consumption 
// by checking the flashing  light of the power meter. 
// One flash should be 1 w/h 
// 
// Updated 2010/02/09 Lionel D.
// Datas are sent via RF module
//
// 06/10/10 - Measurement from phototrans - Lionel

// Here is the token
#define DEVICEID "5d47051f-d265-4e85-9316-b662ed3041f"

// include the library code:
//#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
//LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

// include the virtualwire libary code for RF comm
#include <VirtualWire.h>
#undef int
#undef abs
#undef double
#undef float
#undef round

#include <stdlib.h> 

// Include files for clock DS1307 library 
#include <WProgram.h> 
#include <Wire.h> 
#include <DS1307.h> 
#include <SCP1000.h>

// Include files for MsTimer2 library 
#include <MsTimer2.h> 

/// The PIN to power the SD card shield 
//#define MEM_PW 9

// The PIN to put a led indicating a TX 
#define RF_LED 9

// The PIN to power the RF-TX module 
#define RF_PW 3 

// shield pinouts
#define LED_GREEN 3 
#define LED_BLUE 4
#define LED_RED 2

#define SCP1000_PIN 10
#define AIR 0 // AIRQ
#define LUX 1 // LUX
#define NOI 2 // NOISE
#define HUM 3 // HUMIDITY

SCP1000 scp1000(SCP1000_PIN);
//

//unsigned long timer=3600000; // Log file is written every 60 minutes (3600000)  (normal value) 
unsigned long timer=60000; // Log is written every 60s (debug value)
unsigned long flash=0; 
int threshold=300;     // If photoresistor read more than this value, it count a flash 
int writeLog=0; 

void flushCounter(void);
char* getTIME(char *);

// Arduino setup routine 
void setup(void)  
{

  // shield config
  pinMode (LED_RED, OUTPUT);
  pinMode (LED_GREEN, OUTPUT);
  pinMode (LED_BLUE, OUTPUT);

  // This is to power on the RF Module 
  pinMode(RF_PW, OUTPUT); 
  pinMode(RF_LED, OUTPUT); 

  // Initialize timer 
  MsTimer2::set(timer, flushCounter); 
  MsTimer2::start(); 

  Serial.begin(9600);       // FIXME 
  Serial.println("TX setup");  // Debugging only

  // Initialise the IO and ISR (RF)
  //   vw_set_ptt_inverted(true); // Required for DR3100 (RF)
  vw_setup(1200);	 // Bits per sec (RF)
  vw_set_tx_pin(2); // set the TX pin to pin 2 (lib default is pin 12)

  scp1000.init();

  // set up the LCD's number of rows and columns: 
  //lcd.begin(16, 2);

  // Enable to set up external clock - Uncomment to set DS1307
  // format is (second,minute,hour,day of the week,day,month,year)
  //setClock(0,20,19,6,9,2,10); 
} 

// Main 
void loop(void)  
{ 
    int air=0;
    int lux=0; 
    int noi=0; 
    int hum=0;
    int baro=0; 
    int temp=0;

  //  Serial.println(analogRead(PHOTO_IN));  // FIXME 

  // Send the flash # if the interrupt has been called 
//  if (writeLog==1) 
//  { 

    char buffer[76];
    char timestamp[15];

    //power ON the RF module
    digitalWrite(RF_PW, HIGH); 
    digitalWrite(LED_BLUE, HIGH); // Flash a light on pin RF_LED to show transmitting (DEBUG)

    // read sensors
    air = analogRead(AIR);
    lux = analogRead(LUX);
    noi = 1024-analogRead(NOI); // inverse the value
    hum = analogRead(HUM);
    scp1000.readSensor();
    baro = (int)(scp1000.BaroP*100);
    temp = (int)(scp1000.TempC*10);
    
    Serial.print("air: ");
    Serial.print(air);
    Serial.print(", lux: ");
    Serial.print(lux);
    Serial.print(", noi: ");
    Serial.print(noi);
    Serial.print(", hum: ");
    Serial.print(hum);
    Serial.print(", baro: ");
    Serial.print(baro);
    Serial.print(", temp: ");
    Serial.println(temp);

  //strcat(buffer,getClock(timestamp)); 
  //snprintf(buffer+36, 15, "%s", getTIME(timestamp));
//  snprintf(buffer+50, 11, "%010lu", (unsigned long)((flash*100)*(3600000/timer)));

  snprintf(buffer, 36, "%s", DEVICEID);
  snprintf(buffer+35, 26, "%04i%04i%04i%04i%05i%04i", air,lux,noi,hum,baro,temp);
  buffer[60]=0; 
   // snprintf(buffer, 3, "%s", "42");
    Serial.print(" Buffer : ");
    Serial.println(buffer);

    Serial.print("Sending datagram: ");

    vw_send((uint8_t *)buffer, strlen(buffer));
    vw_wait_tx(); // Wait until the whole message is gone

    Serial.println("done.");


    //power OFF the RF module
    digitalWrite(RF_PW, LOW); 
    digitalWrite(LED_BLUE, LOW); // Flash a light on pin RF_LED to show transmitting (DEBUG)

    writeLog=0; 
    flash=0;  
//  } 

  delay(10000); 
} 

///////////////// 
// Subroutines // 
///////////////// 

// Get the timestamp from the external clock 
char* getTIME(char *timeStr) 
{
  snprintf(timeStr, 15, "%04i%02i%02i%02i%02i%02i",RTC.get(DS1307_YR,true),RTC.get(DS1307_MTH,false),RTC.get(DS1307_DATE,false),RTC.get(DS1307_HR,false),RTC.get(DS1307_MIN,false),RTC.get(DS1307_SEC,false));
  return timeStr;
}

// Write data to log file named data.log 

/*
Placer une fonction ecriture SD par là
 */

// Routine executed by the timer interrupt. 
void flushCounter(void) 
{ 
  writeLog=1; 
} 

