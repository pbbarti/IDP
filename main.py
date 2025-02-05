from sensors import LineFollowingSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from navigation import navigate
from motion import measure_sensors, drive_forward, turn_in_place
from time import sleep
from drop_off import drop_off

# Create instances of Motors
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)
linear_actuator = Linear_Actuator(direction_pin=0, speed_pin=1)

# Create instances of LineFollowingSensor
sensors = (LineFollowingSensor(pin=18),LineFollowingSensor(pin=19),LineFollowingSensor(pin=20),LineFollowingSensor(pin=21))

# Give mapping directions
depot_1_to_D = ['straight','straight','left','left']
D_to_depot_1 = ['right','straight','straight','straight']

while True:
    navigate(depot_1_to_D, left_motor, right_motor, sensors)
    drop_off(sensors, left_motor, right_motor, linear_actuator, 'left', 2)
    navigate(D_to_depot_1, left_motor, right_motor, sensors)
    turn_in_place('right', sensors, left_motor, right_motor)
    

