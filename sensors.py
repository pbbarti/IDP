import struct
from time import sleep, time
import machine
from machine import Pin, ADC


### QR CODE READER ###

## This class is for a QR code reader that 
## uses I2C to communicate with the sensor
## and returns the QR code message
## once the message is read

class QRCodeReader:
    ## NOT INCORRECT CONNECTIONS WILL DESTROY THE SENSOR. CHECK WITH BENCH MULTIMETER BEFORE POWER/USE
    ## Red---3v3
    ## Black---ground
    ## Blue---sda
    ## Yellow---scl
    def __init__(self, i2c, address, delay=0.05):
        self.i2c = i2c
        self.address = address
        self.delay = delay
        self.length_offset = 0
        self.length_format = "H"
        self.message_offset = self.length_offset + struct.calcsize(self.length_format)
        self.message_size = 254
        self.message_format = "B" * self.message_size
        self.i2c_format = self.length_format + self.message_format
        self.i2c_byte_count = struct.calcsize(self.i2c_format)

    def read_message(self):
        sleep(self.delay)
        read_data = self.i2c.readfrom(self.address, self.i2c_byte_count)
        message_length, = struct.unpack_from(self.length_format, read_data, self.length_offset)
        message_bytes = struct.unpack_from(self.message_format, read_data, self.message_offset)

        if message_length == 0:
            return None

        try:
            message_string = bytearray(message_bytes[0:message_length]).decode("utf-8")
            return message_string
        except:
            return None

    def run(self):
        while True:
            message = self.read_message()
            if message:
                return message

## How to set up for the Pico and run

# i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))
# qr_code_reader = QRCodeReader(i2c, 0x0C)
# qr_code_reader.run()

### ULTRASOUND SENSOR ###

class UltrasoundSensor:
    def __init__(self, pin, max_range=520, adc_resolution=65535.0, delay=0.05):
        self.sensor_pin = ADC(pin)
        self.max_range = max_range
        self.adc_resolution = adc_resolution
        self.delay = delay

    def read_distance(self):
        sensity_t = self.sensor_pin.read_u16()  # Read 16-bit ADC value (0-65535)
        dist_t = sensity_t * self.max_range / self.adc_resolution  # Convert to distance in cm
        return dist_t


## How to create an instance of the 
## UltrasoundSensor class and run it

# ultrasound_sensor = UltrasoundSensor(pin=26)
# ultrasound_sensor.read_average_distance()

### LINE FOLLOWING SENSOR ###

## This class is for a line following sensor
## read value function reads and 
## returns 1 if the sensor is on white
## and 0 if it is on black

class LineFollowingSensor:
    def __init__(self, pin):
        self.sensor_pin = Pin(pin, Pin.IN)

    def read_value(self):
        return self.sensor_pin.value()