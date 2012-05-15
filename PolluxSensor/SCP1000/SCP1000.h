/**
* SCP1000 Library
*
*
* Manages communication with SCP1000 barometric pressure & temperature sensor
*
*/
#ifndef SCP1000_h
#define SCP1000_h

#include "Arduino.h"


class SCP1000
{
	public:
		float TempC;	// DegC
		float BaroP;	// in hPa (mbar)

		SCP1000(const byte selectPin);
		void init();
		void readSensor();
		void resetSensor();
		void setStandby();
		void setRunMode();


	private:
		// I/O Pins
		byte _selectPin;

		void readPressure();
		void readTemperature();
		unsigned int read_register(byte register_name, byte numBytes);
		void write_register(byte register_name, byte data);
		byte spi_transfer(volatile byte data);
};

#endif
  
