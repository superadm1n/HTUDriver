from distutils.core import setup

description = '''THis module is designed to act as a driver for interacting with an Adafruit HTU21D-F
It uses I2C to communicate with the module'''

setup(
    name='HTUDriver',
    version='1.0.0',
    packages=['HTUDriver'],
    keywords='Adafruit ht21d-f temperature humidity sensor',
    url='https://github.com/superadm1n/HTUDriver',
    license='MIT',
    author='Kyle Kowalczyk',
    author_email='kowalkyl@gmail.com',
    description='Driver for HTU21D-F',
    long_description=description,
    install_requires=['pigpio==1.40.post1'],
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ]
)