from sensors import LineFollowingSensor
from motors import Motor_Right, Motor_Left
from motion import measure_sensors, drive_forward, move_forward_and_turn

# Create instances of Motors
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)

# Create instances of LineFollowingSensor
LineFollowingSensor_1 = LineFollowingSensor(pin=21)
LineFollowingSensor_2 = LineFollowingSensor(pin=20)
LineFollowingSensor_3 = LineFollowingSensor(pin=19)
LineFollowingSensor_4 = LineFollowingSensor(pin=18)

# Give mapping directions
mapping = ['left','left','straight','left','left']

while True:
    for direction in len(mapping):
        sensor_state = measure_sensors(LineFollowingSensor_1, LineFollowingSensor_2, LineFollowingSensor_3, LineFollowingSensor_4)
        drive_forward(sensor_state, left_motor, right_motor)
        if sensor_state in ['1110','1111'] and mapping[direction] == 'left':
            move_forward_and_turn('left', left_motor, right_motor)
        elif sensor_state in ['']
    





