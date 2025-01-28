from sensors import LineFollowingSensor
from motors import Motor

# Create LineFollowingSensors array by creating instances of LineFollowingSensor
LineFollowingSensors = [LineFollowingSensor(pin=i) for i in range(1, 5)]  

# Create instances of Motor
left_motor = Motor(direction_pin=7, speed_pin=6)
right_motor = Motor(direction_pin=8, speed_pin=9)



