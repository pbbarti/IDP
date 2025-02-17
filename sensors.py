import struct
from time import sleep
from machine import Pin, ADC


### QR CODE READER ###

# This class is for a QR code reader that 
# uses I2C to communicate with the sensor
# and returns the QR code message
# once the message is read

class QRCodeReader:
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

    # Function to read the message from the QR code reader
    # and return it as a string if it is read properly
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

### ULTRASOUND SENSOR ###

# This class is for an ultrasound sensor
# that reads the distance to an object
# and returns it in centimeters

class UltrasoundSensor:
    def __init__(self, pin, max_range=520, adc_resolution=65535.0, delay=0.05):
        self.sensor_pin = ADC(pin)
        self.max_range = max_range
        self.adc_resolution = adc_resolution
        self.delay = delay

    # Function to read the distance from the ultrasound sensor
    # and return it in centimeters
    def read_distance(self):
        sensitivity = self.sensor_pin.read_u16()                                      # Read 16-bit ADC value (0-65535)
        distance = sensitivity * self.max_range / self.adc_resolution                 # Convert to distance in cm
        return distance

### LINE FOLLOWING SENSOR ###

# This class is for a line following sensor
# that reads its value and 
# returns 1 if the sensor is on white surface
# and 0 if it is on black surface

class LineFollowingSensor:
    def __init__(self, pin):
        self.sensor_pin = Pin(pin, Pin.IN)

    def read_value(self):
        return self.sensor_pin.value()