from sensors import LineFollowingSensor, QRCodeReader, UltrasoundSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from navigation import navigate
from motion import measure_sensors, drive_forward, turn_in_place
from drop_off import drop_off
from pick_up import pick_up
from machine import Pin, I2C
from time import sleep
import time
from navigationv2 import routes, choose_route, leave_depot

# Create instances of Motors
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)
linear_actuator = Linear_Actuator(direction_pin=0, speed_pin=1)

# Create instances of LineFollowingSensor
sensors = (LineFollowingSensor(pin=22), LineFollowingSensor(pin=21), LineFollowingSensor(pin=17), LineFollowingSensor(pin=16))

# Create instance of QR code reader
i2c = I2C(1, scl=Pin(19), sda=Pin(18))
qr_code_reader = QRCodeReader(i2c, 0x0C)

# Create instance of Distance sensor
ultrasound_sensor = UltrasoundSensor(pin=26)

# Create instance of PIN OUT for LED circuit
led = Pin(14, Pin.OUT)

# Create instance of PIN IN for button operation
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

interrupt_flag = 0
debounce_time = 0

def callback(button):
    global interrupt_flag, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        interrupt_flag = 1
        debounce_time = time.ticks_ms()

button.irq(trigger=Pin.IRQ_RISING, handler=callback)

while True:
    if interrupt_flag is 1:
        interrupt_flag = 0
        # add function to move out of starting zone manually here
        led.value(1)
        navigate(routes('start_to_depot_1'), left_motor, right_motor, sensors)
        for i in range(3):
            qr_message = pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)
            route = choose_route(qr_message)
            navigate(route[0], left_motor, right_motor, sensors)
            drop_off(sensors, left_motor, right_motor, linear_actuator, leave_depot(qr_message)[0], leave_depot(qr_message)[1])
            navigate(route[1], left_motor, right_motor, sensors)
        navigate(routes('depot_1_to_depot_2'), left_motor, right_motor, sensors)
        for i in range(3):
            qr_message = pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)
            route = choose_route(qr_message)
            navigate(route[0], left_motor, right_motor, sensors)
            drop_off(sensors, left_motor, right_motor, linear_actuator, leave_depot(qr_message)[0], leave_depot(qr_message)[1])
            navigate(route[1], left_motor, right_motor, sensors)
        navigate(routes('depot_2_to_start'), left_motor, right_motor, sensors)
        led.value(0)
        # add function to move into starting zone manually here