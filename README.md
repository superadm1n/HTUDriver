# HTUDriver

This module is designed to be used as a driver for an Adafruit
HTU21D-F temperature and humidity sensor.


### Prerequisites

I2C communication enabled on Raspberry Pi.

pigpio


### Installation
Issue the following commands to install this driver into your project

```
pip install git+https://github.com/superadm1n/HTUDriver
```

### Using Driver
Below is example code for using the driver to read the temperature
and humidity.

```
import HTUDriver
with HTUDriver.Driver() as sensor:

    # gets temperature and humidity
    temp = sensor.get_temperature()
    humidity = sensor.get_humidity()

    # prints values to the user

    print('Temperature: {}'.format(temp))
    print('Humidity: {}'.format(humidity)

#EOF
```


## Author

* **Kyle Kowalczyk**  [SmallGuysIT](https://smallguysit.com)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

