from sensors import LineFollowingSensor
from time import sleep

## This function takes a list of sensors and returns a list of their values
def measure_sensors(LineFollowingSensor_1, LineFollowingSensor_2, LineFollowingSensor_3, LineFollowingSensor_4 ):
    reading = []
    reading.append(LineFollowingSensor_1.read_value())
    reading.append(LineFollowingSensor_2.read_value())
    reading.append(LineFollowingSensor_3.read_value())
    reading.append(LineFollowingSensor_4.read_value())
    return reading


## This function takes a list of sensors measurements
## and two motor instances as arguments
## and based on the values of sensors sets 
## driving parameters for motors

def drive_forward(sensors_state, left_motor, right_motor):
    # Convert readings to a binary number of sensors states
    sensor_state = ''.join(map(str, sensors_state))
    
    # Define motor actions for each sensor state in a binary map   -  !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
    actions = {
        '0000': ('forward', 0, 'forward', 0), #bad
        '0001': ('forward', 0, 'forward', 0), #bad
        '0010': ('forward', 55, 'forward', 45), #correct to right
        '0011': ('forward', 55, 'forward', 45), #correct to right + possible turn right
        '0100': ('forward', 45, 'forward', 55), #correct to left
        '0101': ('forward', 0, 'forward', 0), #bad
        '0110': ('forward', 70, 'forward', 70), #forward
        '0111': ('forward', 0, 'forward', 0), #possible turn right
        '1000': ('forward', 0, 'forward', 0), #bad
        '1001': ('forward', 0, 'forward', 0), #bad
        '1010': ('forward', 0, 'forward', 0), #bad
        '1011': ('forward', 0, 'forward', 0), #bad
        '1100': ('forward', 45, 'forward', 55), #correct left + possible turn left
        '1101': ('forward', 0, 'forward', 0), #bad
        '1110': ('forward', 0, 'forward', 0), #possible turn left
        '1111': ('forward', 0, 'forward', 0), #possible turn right or left
    }
    
    # Get the action for the current sensor state
    left_action, left_speed, right_action, right_speed = actions[sensor_state]
    
    # Set the motors based on the action
    left_motor.set_motor(left_action, left_speed)
    right_motor.set_motor(right_action, right_speed)

    # action delay
    sleep(0.1)

## How to set up for the Pico and run

# Create LineFollowingSensors array by creating instances of LineFollowingSensor

#LineFollowingSensors = [LineFollowingSensor(pin=i) for i in range(1, 5)]  

# !!!make sure to assign corresponding GPIO pins to the sensors!!!

# Create instances of Motor

#left_motor = Motor(direction_pin=7, speed_pin=6)
#right_motor = Motor(direction_pin=8, speed_pin=9)

# !!!make sure to assign corresponding GPIO pins to the motors!!!

#while True:
    #sensors_state = measure_sensors(LineFollowingSensors)
    #drive_forward(sensors_state, left_motor, right_motor)


## This function takes both motor instances as arguments
## and stops them

def stop_motors(left_motor, right_motor):
    left_motor.off()
    right_motor.off()


## This function takes a direction, left motor instance, and right motor instance as arguments
## and turns the robot in place in the given direction

def turn_in_place(direction, left_motor, right_motor):
    # Calibrated distance needed for a 90-degree turn
    calibrated_distance = 70  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!

    if direction == "right":
        left_motor.set_motor("forward", 50)
        right_motor.set_motor("reverse", 50)
    elif direction == "left":
        left_motor.set_motor("reverse", 50)
        right_motor.set_motor("forward", 50)
    else:
        raise ValueError("Invalid direction. Use 'right' or 'left'.")

    # Calibrate the time needed to turn 90 degrees based on the distance
    # This is a placeholder value and should be adjusted based on actual calibration
    time_to_turn = calibrated_distance / 50  # Assuming 50 is the speed and distance is in distance unit

    sleep(time_to_turn)

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

## How to set up for the Pico and run

# Create instances of Motor

#left_motor = Motor(direction_pin=7, speed_pin=6)
#right_motor = Motor(direction_pin=8, speed_pin=9)

# !!!make sure to assign corresponding GPIO pins to the motors!!!

# Turn right

#turn_in_place("right")
#sleep(1)

# Turn left

#turn_in_place("left")
#sleep(1)

## This function takes a direction, left motor instance, and right motor instance as arguments
## and turns the robot in place in the given direction
## then moves forward a bit after turning

def move_forward_and_turn(direction, left_motor, right_motor):
    # Calibrated distance needed for a 90-degree turn
    calibrated_turn_distance = 10  #!!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
    # Calibrated distance to move forward after turning
    calibrated_forward_distance = 5  #!!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
                                     # such that it moves forward a distance from sensors to axis

    # Move forward first
    left_motor.set_motor("forward", 50)
    right_motor.set_motor("forward", 50)
    sleep(calibrated_forward_distance)

    # Then turn in place
    if direction == "right":
        left_motor.set_motor("forward", 50)
        right_motor.set_motor("reverse", 50)
    elif direction == "left":
        left_motor.set_motor("reverse", 50)
        right_motor.set_motor("forward", 50)
    else:
        raise ValueError("Invalid direction. Use 'right' or 'left'.")

    # Calibrate the time needed to turn 90 degrees based on the distance
    sleep(calibrated_turn_distance)

    # Stop the motors after turning
    left_motor.set_motor("stop")
    right_motor.set_motor("stop")

## How to set up for the Pico and run

# Create instances of Motor

#left_motor = Motor(direction_pin=7, speed_pin=6)
#right_motor = Motor(direction_pin=8, speed_pin=9)

# !!!make sure to assign corresponding GPIO pins to the motors!!!

# Turn right and move forward

#turn_and_move_forward("right")
#sleep(1)

# Turn left and move forward

#turn_and_move_forward("left")
#sleep(1)

