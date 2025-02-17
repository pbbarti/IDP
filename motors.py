from machine import Pin, PWM
from time import sleep


### MOTOR MOTION ###

# This class is for operating motors
# it allows to set the direction and speed of motor
# and make it act accordeingly
# also allows to turn off the motor
# Motor_Right and Motor_Left classes are used to control the right and left motors respectively

class Motor_Right:
    def __init__(self, direction_pin, speed_pin):
        self.m1Dir = Pin(direction_pin, Pin.OUT)            # set motor direction !!! GPIO !!!
        self.pwm1 = PWM(Pin(speed_pin))                     # set speed !!! PWM PIN  !!!
        self.pwm1.freq(1000)                                # set max frequency
        self.pwm1.duty_u16(0)                               # set duty cycle

    # Function to set the motor direction and speed
    def set_motor(self, direction, speed):
        if direction == "forward":
            self.m1Dir.value(1)                             # forward = 1 reverse = 0, those are calibrated with respect to AGV motion direction for easier further usage
        elif direction == "reverse":
            self.m1Dir.value(0)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'reverse'.")
        
        if 0 <= speed <= 100:
            self.pwm1.duty_u16(int(65535 * speed / 100))    # speed range 0-100 motor speed is set as a percentage of max speed
        else:
            raise ValueError("Invalid speed. Use a value between 0 and 100.")

    def off(self):
        self.pwm1.duty_u16(0)

# class with the same functionality as Motor_Right but for the left motor
class Motor_Left:
    def __init__(self, direction_pin, speed_pin):
        self.m1Dir = Pin(direction_pin, Pin.OUT)
        self.pwm1 = PWM(Pin(speed_pin))
        self.pwm1.freq(1000)
        self.pwm1.duty_u16(0) 

    def set_motor(self, direction, speed):
        if direction == "forward":
            self.m1Dir.value(0)  
        elif direction == "reverse":
            self.m1Dir.value(1)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'reverse'.")
        
        if 0 <= speed <= 100:
            self.pwm1.duty_u16(int(65535 * speed / 100)) 
        else:
            raise ValueError("Invalid speed. Use a value between 0 and 100.")

    def off(self):
        self.pwm1.duty_u16(0)

### LINEAR ACTUATOR MOTION ###

# This class is for operating a linear acutator
# it allows to set the direction and required extension of the actuator
# and make it act accordeingly with its maximum speed and switching off after finishing
# also allows to fully retract the actuator

class Linear_Actuator:
    MAX_SPEED = 7  # mm/s

    def __init__(self, direction_pin, speed_pin):
        self.direction_pin = Pin(direction_pin, Pin.OUT)        # set actuator direction
        self.pwm = PWM(Pin(speed_pin))                          # set speed
        self.pwm.freq(1000)                                     # set max frequency
        self.pwm.duty_u16(0)                                    # set duty cycle

    def set_actuator(self, extension):
        if extension < 0:
            self.direction_pin.value(0)                         # retract = 0 extend = 1
            extension = abs(extension)                          # take absolute value of extension in case of retracting
        else:
            self.direction_pin.value(1)

        if 0 <= extension <= 50:
            self.pwm.duty_u16(int(65535))                       # use max speed for extending and retracting
            sleep(extension / self.MAX_SPEED)                   # time needed for given extension
            self.off()
    
    # Function to fully retract the actuator
    def fully_retract(self):
        self.direction_pin.value(0)
        self.pwm.duty_u16(int(65535))
        sleep(50/self.MAX_SPEED)
        self.off()

    # Function to stop the actuator
    def off(self):
        self.pwm.duty_u16(0)