# Info: Main file to run the robot. This file will be run on the robot to complete the task.
# The robot will navigate through the course, pick up and drop off packages, and return to the starting area.
# First import the necessary classes, functions and classes.

from sensors import LineFollowingSensor, QRCodeReader, UltrasoundSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from motion import turn_in_place_depot, start_area, start_area_finish
from navigation import navigate,  routes, choose_route, leave_depot
from drop_off import drop_off
from pick_up import pick_up
from machine import Pin, I2C
from time import sleep
import time


# Create instances of Motors with appropriate GPIO pins assingments
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)
linear_actuator = Linear_Actuator(direction_pin=0, speed_pin=1)

# Create instances of LineFollowingSensor with appropriate GPIO pins assingments
sensors = (LineFollowingSensor(pin=22), LineFollowingSensor(pin=21), LineFollowingSensor(pin=17), LineFollowingSensor(pin=16))

# Create instance of QR code reader with I2C communication
i2c = I2C(1, scl=Pin(19), sda=Pin(18))
qr_code_reader = QRCodeReader(i2c, 0x0C)

# Create instance of Distance sensor with appropriate GPIO pin assingment   
ultrasound_sensor = UltrasoundSensor(pin=26)

# Create instance of PIN OUT for LED circuit
led = Pin(14, Pin.OUT)

# Create instance of PIN IN for button operation
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# Create global variables for interrupt handling used to run the programme on button press
interrupt_flag = 0
debounce_time = 0

# Create interrupt handler for button press
def callback(button):
    global interrupt_flag, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        interrupt_flag = 1
        debounce_time = time.ticks_ms()

# Assign interrupt handler to the button
button.irq(trigger=Pin.IRQ_RISING, handler=callback)

# Main loop to run the robot
while True:

    # Check if the interrupt flag is set to 1 and run the robot
    if interrupt_flag is 1:

        # Reset the interrupt flag
        interrupt_flag = 0

        # Leave the start area
        start_area(left_motor, right_motor, sensors)

        # Switch on the LED to indicate the robot is running
        led.value(1)

        # Navigate to the first depot
        navigate(routes['start_to_depot_1'], left_motor, right_motor, sensors)

        # Loop through the depot_1 4 times to pick up and drop off all packages
        for i in range(4):
            
            # For two furthest packages additional alinging is necessary for proper QR code scanning
            if i >= 2:                                                                                 ### TURN IN PLACE FOR DEPOT IS TOO LITTLE ###
                left_motor.set_motor('forward',80)
                right_motor.set_motor('forward',80)
                sleep(0.6)
                right_motor.off()
                left_motor.off()
            
            # Pick up the package and get the destination
            qr_message = pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)

            # Choose the route based on the QR code message read
            route = choose_route(qr_message)

            # Leaving the depot for two furthest packages requires additional alinging
            if i >= 2:
                left_motor.set_motor('forward',80)
                right_motor.set_motor('forward',80)
                sleep(0.8)
                left_motor.off()
                right_motor.off()
            
            # Navigate to the destination
            navigate(route[0], left_motor, right_motor, sensors)

            # Drop off the package and leave the destination based on leaving paramenters
            drop_off(sensors, left_motor, right_motor, linear_actuator, leave_depot(qr_message)[0], leave_depot(qr_message)[1])

            # Navigate back to the depot
            navigate(route[1], left_motor, right_motor, sensors)

        # When all packages are picked up and dropped off use depot_1 to navigate back to the start area
        # Additional alinging in depot is necessary for proper navigation
        left_motor.set_motor('forward',80)
        right_motor.set_motor('forward',80)
        sleep(1)
        left_motor.off()
        right_motor.off()

        # Turn in place to face depot_1 leaving
        turn_in_place_depot('right', left_motor, right_motor)

        # Navigate back to the start area from depot_1
        navigate(routes['depot_1_to_start'], left_motor, right_motor, sensors)

        # Switch off the LED to indicate the robot has finished
        led.value(0)

        # Return to the start area and stop the robot
        start_area_finish(left_motor, right_motor)