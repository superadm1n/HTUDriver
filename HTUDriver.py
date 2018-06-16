'''
MIT License

Copyright (c) 2018 Kyle Kowalczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------------------------------------------------------------------------------

Description:

Python Driver for the Adafruit HT21D-F temperature and humidity sensor

The ht21d-f relies on i2c to communicate with the device so this driver communicates
to the hardware via an I2C bus.

Author: Kyle Kowalczyk
'''
import time
import pigpio

class Driver:

    FAHRENHEIT = 0
    CELSIUS = 1

    def __init__(self, bus=1, resetOninit=True):

        '''

        :param bus: i2c bus value, RasPi revA is 0, otherwise 1 should work
        :param resetOninit: if true will send a reset command to the bus
        '''

        self.pi = pigpio.pi()

        # HTU21D-F i2c address
        self.addr = 0x40
        self.bus = bus

        if resetOninit is True:
            self.device_reset()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def cel_to_faren(self, celsius):

        '''Used to convert celsius to fahrenheit

        :param celsius: degrees in celsius
        :return: temperature supplied in fahrenheit
        '''
        return (celsius * 1.8) + 32

    def _open_bus(self):

        '''
        Method to open the i2c bus to communicate
        :return:
        '''

        bus = self.pi.i2c_open(self.bus, self.addr)
        return bus

    def _close_bus(self, busObj):

        '''
        Method to close i2c bus after communication
        :param busObj: bus object to close
        :return:
        '''

        self.pi.i2c_close(busObj)

    def _write_handler(self, busObj, command):

        '''
        Handles writing data to the i2c bus
        :param busObj: bus object to write to
        :param command: command to write to the bus
        :return:
        '''

        # send read temp command
        self.pi.i2c_write_byte(busObj, command)
        # can take up to 50ms; adding in and extra .005 seconds for padding
        time.sleep(0.055)


    def _read_handler(self, busObj):

        '''
        Handles reading data from the i2c bus.
        :param busObj: bus object to read from
        :return: data that was returned from bus
        '''

        # reads the bytes off of the i2c bus
        (count, byteArray) = self.pi.i2c_read_device(busObj, 3)
        # close the i2c bus
        self.pi.i2c_close(busObj)

        msb = byteArray[0]
        lsb = byteArray[1]

        return msb, lsb


    def device_reset(self):

        '''Resets the HTU21D-F

        :return:
        '''

        resetCommand = 0xFE

        # opens the bus
        bus = self._open_bus()

        # sends a reset command
        self._write_handler(bus, resetCommand)

        # closes bus
        self._close_bus(bus)

        # reset takes 15ms so let's give it some time
        time.sleep(0.2)

    def get_temperature(self, returnAs=FAHRENHEIT):

        '''Gets the temperature reading from HTU21D-F.

        :param returnAs: fahrenheit or celsius
        :return: temperature in fahrenheit or celsius
        :rtype: float
        '''

        readTempcommand = 0xE3

        # opens up bus
        bus = self._open_bus()

        # sends command to bus to read the temperature
        self._write_handler(bus, readTempcommand)
        msb, lsb = self._read_handler(bus)

        # analyzes the data that was returned back
        temperatureReading = float((msb * 256) + lsb)

        # Algorithm for interpreting the data as stated in the datasheet
        temperature = round(((temperatureReading / 65536) * 175.72) - 46.85, 2)

        # if the data should be returned as fahrenheit convert from celsius if not just return the temp
        if returnAs is self.FAHRENHEIT:
            return round(self.cel_to_faren(temperature), 2)  # rounds number down to only 2 digits pas decimal point
        else:
            return temperature

    def get_humidity(self):

        '''Gets humidity reading from the HTU21D-F

        :return:
        '''

        readHumiditycommand = 0xE5

        # opens up the bus
        bus = self._open_bus()

        # sends command to read the humidity
        self._write_handler(bus, readHumiditycommand)

        # reads data returned from the bus
        msb, lsb = self._read_handler(bus)

        # analyzes the data that was returned

        # combine both bytes into a single float
        humidityReading = float((msb * 256) + lsb)

        # algorithm for analyzing value as shown in the datasheet
        humidityValue = ((humidityReading / 65536) * 125) - 6

        return round(humidityValue, 2)

if __name__ == '__main__':


    '''
    Below is an example of using the driver to get data and print it out the 
    user.
    '''

    with HTUDriver() as sensor:

        while True:
            try:
                # gets temperature and humidity
                temp = sensor.get_temperature()
                humid = sensor.get_humidity()

                # prints values to the user
                print('Temp: {}\nHumidity {}'.format(temp, humid))
                time.sleep(1)

            # breaks out of loop on control+c
            except KeyboardInterrupt:
                break
