from sensors import LineFollowingSensor, QRCodeReader, UltrasoundSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from navigation import navigate,  routes, choose_route, leave_depot, start_area
from motion import measure_sensors, drive_forward, turn_in_place
from drop_off import drop_off
from pick_up import pick_up
from machine import Pin, I2C
from time import sleep
import time


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

#linear_actuator.set_actuator(1)
led.value(0)

while True:
    if interrupt_flag is 1:
        interrupt_flag = 0
        start_area(left_motor, right_motor, sensors)
        led.value(1)
        navigate(routes['start_to_depot_1'], left_motor, right_motor, sensors)
        for i in range(2):
            if i > 2:
                left_motor.set_motor('forward',80)
                right_motor.set_motor('forward',80)
                sleep(1.1)
            qr_message = pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)
            route = choose_route(qr_message)
            if i > 2:
                navigate('straight',left_motor, right_motor, sensors)
            navigate(route[0], left_motor, right_motor, sensors)
            drop_off(sensors, left_motor, right_motor, linear_actuator, leave_depot(qr_message)[0], leave_depot(qr_message)[1])
            navigate(route[1], left_motor, right_motor, sensors)
        left_motor.set_motor('forward',80)
        right_motor.set_motor('forward',80)
        sleep(1.5)
        turn_in_place('right', sensors, left_motor, right_motor)
        navigate(routes['depot_1_to_start'], left_motor, right_motor, sensors)
        led.value(0)
        left_motor.set_motor('forward',70)
        right_motor.set_motor('forward',70)
        sleep(1)
        left_motor.off()
        right_motor.off()
#         #for i in range(3):
#             #qr_message = pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)
#             #route = choose_route(qr_message)
#             #navigate(route[0], left_motor, right_motor, sensors)
#             #drop_off(sensors, left_motor, right_motor, linear_actuator, leave_depot(qr_message)[0], leave_depot(qr_message)[1])
#             #navigate(route[1], left_motor, right_motor, sensors)
#         #navigate(routes('depot_2_to_start'), left_motor, right_motor, sensors)
#         #led.value(0)
#         #start_area(left_motor, right_motor, sensors)
