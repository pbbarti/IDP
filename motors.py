from machine import Pin, PWM
from time import sleep


### MOTOR MOTION ###

## This class is for operating motors
## it allows to set the direction and speed of motor
## and make it act accordeingly
## also allows to turn off the motor


class Motor_Right:
    def __init__(self, direction_pin, speed_pin):
        self.m1Dir = Pin(direction_pin, Pin.OUT) # set motor direction !!! GPIO !!!
        self.pwm1 = PWM(Pin(speed_pin)) # set speed !!! PWM PIN  !!!
        self.pwm1.freq(1000) # set max frequency
        self.pwm1.duty_u16(0) # set duty cycle

    def set_motor(self, direction, speed):
        if direction == "forward":
            self.m1Dir.value(0) # forward = 0 reverse = 1 
        elif direction == "reverse":
            self.m1Dir.value(1)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'reverse'.")
        
        if 0 <= speed <= 100:
            self.pwm1.duty_u16(int(65535 * speed / 100)) # speed range 0-100 motor 1
        else:
            raise ValueError("Invalid speed. Use a value between 0 and 100.")

    def off(self):
        self.pwm1.duty_u16(0)


class Motor_Left:
    def __init__(self, direction_pin, speed_pin):
        self.m1Dir = Pin(direction_pin, Pin.OUT) # set motor direction !!! GPIO !!!
        self.pwm1 = PWM(Pin(speed_pin)) # set speed !!! PWM PIN  !!!
        self.pwm1.freq(1000) # set max frequency
        self.pwm1.duty_u16(0) # set duty cycle

    def set_motor(self, direction, speed):
        if direction == "forward": #forward = 1 reverse = 0
            self.m1Dir.value(1)  
        elif direction == "reverse":
            self.m1Dir.value(0)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'reverse'.")
        
        if 0 <= speed <= 100:
            self.pwm1.duty_u16(int(65535 * speed / 100)) # speed range 0-100 motor 1
        else:
            raise ValueError("Invalid speed. Use a value between 0 and 100.")

    def off(self):
        self.pwm1.duty_u16(0)

### LINEAR ACTUATOR MOTION ###

## This class is for operating a linear acutator
## it allows to set the direction and required extension of the actuator
## and make it act accordeingly with half of its maximum speed and switching off after finishing
## also allows to fully retract the actuator

class Linear_Actuator:
    MAX_SPEED = 7  # mm/s

    def __init__(self, direction_pin, speed_pin):
        self.direction_pin = Pin(direction_pin, Pin.OUT) # set actuator direction
        self.pwm = PWM(Pin(speed_pin)) # set speed
        self.pwm.freq(1000) # set max frequency
        self.pwm.duty_u16(0) # set duty cycle

    def set_actuator(self, extension):
        if extension < 0:
            self.direction_pin.value(0)  # retract
            extension = abs(extension)
        else:
            self.direction_pin.value(1)  # extend

        if 0 <= extension <= 50:
            self.pwm.duty_u16(int(65535))  # always run at half max speed
            sleep(extension / self.MAX_SPEED)  # time to achieve the extension
            self.off()
        else:
            raise ValueError("Invalid extension. Use a value between 0 and 50.")

    def off(self):
        self.pwm.duty_u16(0)

    def fully_retract(self):
        self.direction_pin.value(0)  # retract
        self.pwm.duty_u16(int(65535))  # always run at half max speed
        # Assuming it takes 100 units to fully retract
        sleep(100 / self.MAX_SPEED)
        self.off()