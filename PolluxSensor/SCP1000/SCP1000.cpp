/**
* SCP1000 Library
*
*
* Manages communication with SCP1000 barometric pressure & temperature sensor
*
*/
#include "Arduino.h"
#include "SCP1000.h"

// Class global constants
const byte DataOutPin = 11;
const byte DataInPin = 12;
const byte SPIClockPin = 13;

// Register Addresses
const byte REVID = 0x00;		// ASIC Revision Number
const byte OPREG = 0x03;		// Operation Register
const byte OPSTATUS = 0x04;		// Operation Status
const byte STATUS = 0x07;		// ASIC Status
const byte PRESSURE = 0x1F;		// Pressure 3 MSB
const byte PRESSURE_LSB = 0x20;	// Pressure 16 LSB
const byte TEMP = 0x21;			// 16 bit temp
const byte RSTR = 0x06;			// Soft Reset register

// Mode values
const byte HiResMode = 0x0A;	// Hi Resolution, Constant Readings
const byte StandbyMode = 0x00;	// No operation





SCP1000::SCP1000(const byte selectPin)
{
	// User chosen Slave Select Pin
	_selectPin = selectPin;
}

/* ================ Public methods ================ */

void SCP1000::init()
{
	// Set Pin directions
	pinMode(DataOutPin, OUTPUT);
	pinMode(DataInPin, INPUT);
	pinMode(SPIClockPin,OUTPUT);
	pinMode(_selectPin,OUTPUT);
	digitalWrite(_selectPin,HIGH); //disable device  

	// Set SPI control register
	// SPIE = 0	no interupt
	// SPE = 1	SPI enabled
	// DORD = 0	(MSB first)
	// MSTR = 1 (master)
	// CPOL = 0 (clock idle when low)
	// CPHA = 0 (samples MOSI on rising edge)
	// SPR1 = 1 & SPR0 = 1 (125kHz)
	SPCR = 0b01010011;
	SPSR = 0b00000000;

	delay(100);		// Allow SCP1000 to complete initialization
	setRunMode();

}

/*
 * Fetch values from the sensor
 */
void SCP1000::readSensor()
{
	readTemperature();
	readPressure();
}

/*
 * Send a soft reset
 */
void SCP1000::resetSensor()
{
	write_register(RSTR, 0x01);
	delay(100);		// allow time for reset to complete
}

/*
 * Set sensor to standby mode
 * Stops all sensor operations
 */
void SCP1000::setStandby()
{
	write_register(OPREG, StandbyMode);
}

/*
 * Set sensor to run mode
 */
void SCP1000::setRunMode()
{
	// Set SCP1000 Mode -- Hi resolution, continuous readings
	write_register(OPREG, HiResMode);
}

/* ================ Private methods ================ */

/*
* Reads current pressure value
*/
void SCP1000::readPressure()
{
	unsigned long pressure;

	// Pressure value is in 19-bit unsigned format
	// Value = Pa * 4
	pressure = read_register(PRESSURE, 1);  // Read MSB
	pressure &= 0b00000111;					// mask unused bits
	pressure <<= 16;						// shift into upper word

	pressure  |= read_register(PRESSURE_LSB, 2); // read low word

	// Convert to real pressure in hPa
	BaroP = pressure / 4000.0;

}


/*
* Reads the current temperature value
*/
void SCP1000::readTemperature()
{
	int temp_in;

	// Temperature word is 14-bit signed int = (DegC * 20)
	temp_in = read_register(TEMP, 2);

	// Shift sign bit (bit 13) to proper position for signed int (bit 15)
	// This is equivalent to multiplying by 4, so now temp_in = DegC * 80
	temp_in <<= 2;
	TempC = temp_in / 80.0;		// Convert to real DegC
}

/*
 * Read a register from the device; 1 or 2 bytes
 */
unsigned int SCP1000::read_register(byte register_name, byte numBytes)
{
	unsigned int in_word;

	// SCP1000 registers are either 1 or 2 bytes long
	numBytes = (numBytes > 2) ? 2 : numBytes;  // ensure # of bytes is 0..2

	// SCP1000 command format is 6-bit address, 1-bit R/W, and 1-bit "0"
	register_name <<= 2;		// Shift register address to upper bits
	register_name &= 0b11111100;	//Read command

	digitalWrite(_selectPin,LOW);	// Select SPI Device
	spi_transfer(register_name);	// Send register address to device

	for(; numBytes > 0; --numBytes) {
		in_word <<= 8;					// move existing bits up by one byte
		in_word |= spi_transfer(0x00);	// add next byte
	}

	digitalWrite(_selectPin,HIGH);	// End Communiction

	return(in_word);
}

/*
 * Write single byte to a device register
*/
void SCP1000::write_register(byte register_name, byte data)
{
	//SCP1000 command format is 6-bit address, 1-bit R/W, and 1-bit "0"
	register_name <<= 2;			// Shift register address to upper bits
	register_name |= 0b00000010;		// Write command

	digitalWrite(_selectPin,LOW);	//Select SPI device
	spi_transfer(register_name);	//Send register location
	spi_transfer(data);				//Send value to record into register
	digitalWrite(_selectPin,HIGH);	// End Communication

}

/*
 * Transfer single byte over SPI Bus.  Tx & Rx happen simultaneously
 */
byte SCP1000::spi_transfer(volatile byte data)
{
	SPDR = data;					// Start the transmission
	while (!(SPSR & (1<<SPIF)))		// Wait for the end of the transmission
	{};
	return SPDR;					// return the received byte
}
 
