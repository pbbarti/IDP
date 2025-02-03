from sensors import LineFollowingSensor
from motors import Motor_Right, Motor_Left, Linear_Actuator
from navigation import navigate

# Create instances of Motors
right_motor = Motor_Right(direction_pin=7, speed_pin=6)
left_motor = Motor_Left(direction_pin=4, speed_pin=5)
linear_actuator = Linear_Actuator(direction_pin=0, speed_pin=1)

# Create instances of LineFollowingSensor
sensors = (LineFollowingSensor(pin=18),LineFollowingSensor(pin=19),LineFollowingSensor(pin=20),LineFollowingSensor(pin=21))

# Give mapping directions 
mapping = ['straight','left','straight','left','straight','left','left']

while True:
    navigate(mapping, left_motor, right_motor, sensors)
