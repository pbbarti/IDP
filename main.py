from sensors import LineFollowingSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from navigation import navigate
from motion import drive_forward, measure_sensors, turn_in_place, move_forward_and_turn
from time import sleep

# Create instances of Motors
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)
linear_actuator = Linear_Actuator(direction_pin=0, speed_pin=1)

# Create instances of LineFollowingSensor
LineFollowingSensor_1 = LineFollowingSensor(pin=18)
LineFollowingSensor_2 = LineFollowingSensor(pin=19)
LineFollowingSensor_3 = LineFollowingSensor(pin=20)
LineFollowingSensor_4 = LineFollowingSensor(pin=21)
sensors = (LineFollowingSensor_1,LineFollowingSensor_2,LineFollowingSensor_3,LineFollowingSensor_4)

# Give mapping directions 
mapping = ['straight','left','straight','left','straight','left','left']
depot_1_to_D = ['straight','straight','left','left']

while True:
    navigate(mapping, left_motor, right_motor, sensors)
