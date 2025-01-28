from sensors import LineFollowingSensor
from motors import Motor
from motion import drive_forward, turn_in_place, turn_and_move_forward, stop_motors
from  time import sleep
from motion import measure_sensors

# Create LineFollowingSensors array by creating instances of LineFollowingSensor
LineFollowingSensors = [LineFollowingSensor(pin=i) for i in range(1, 5)]  
# !!!make sure to assign corresponding GPIO pins to the sensors!!!

# Create instances of Motor
left_motor = Motor(direction_pin=7, speed_pin=6)
right_motor = Motor(direction_pin=8, speed_pin=9)
# !!!make sure to assign corresponding GPIO pins to the motors!!!
while True:
    sensors_state = measure_sensors(LineFollowingSensors)
    drive_forward(sensors_state, left_motor, right_motor)
    if sensors_state == "0000": # - !!! ADJUST ACCORDING TO SENSORS PLACEMENT FOR TESTING !!!
        turn_in_place("right", left_motor, right_motor)
        sleep(1)
        turn_in_place("left", left_motor, right_motor)
        sleep(1)
        turn_and_move_forward("right", left_motor, right_motor)
        stop_motors(left_motor, right_motor)