from sensors import LineFollowingSensor
from time import sleep

## This function takes a list of sensors and returns a list of their values
def measure_sensors(sensors):
    return (sensor.read_value() for sensor in sensors)


## This function takes a list of sensors measurements
## and two motor instances as arguments
## and based on the values of sensors sets 
## driving parameters for motors

def drive_forward(sensors_state, left_motor, right_motor):
    # Convert readings to a binary number of sensors states
    sensor_state = ''.join(map(str, sensors_state))
    
    # Define motor actions for each sensor state in a binary map   -  !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
    actions = {
        '0000': ('forward', 50, 'forward', 50),
        '0001': ('forward', 60, 'forward', 40),
        '0010': ('forward', 55, 'forward', 45),
        '0011': ('forward', 70, 'forward', 30),
        '0100': ('forward', 45, 'forward', 55),
        '0101': ('forward', 50, 'forward', 50),
        '0110': ('forward', 60, 'forward', 40),
        '0111': ('forward', 75, 'forward', 25),
        '1000': ('forward', 40, 'forward', 60),
        '1001': ('forward', 45, 'forward', 55),
        '1010': ('forward', 50, 'forward', 50),
        '1011': ('forward', 65, 'forward', 35),
        '1100': ('forward', 30, 'forward', 70),
        '1101': ('forward', 35, 'forward', 65),
        '1110': ('forward', 40, 'forward', 60),
        '1111': ('forward', 50, 'forward', 50),
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
    calibrated_distance = 10  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!

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

def turn_and_move_forward(direction, left_motor, right_motor):
    # Calibrated distance needed for a 90-degree turn
    calibrated_turn_distance = 10  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
    # Calibrated distance to move forward after turning
    calibrated_forward_distance = 5  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!

    if direction == "right":
        left_motor.set_motor("forward", 50)
        right_motor.set_motor("reverse", 50)
    elif direction == "left":
        left_motor.set_motor("reverse", 50)
        right_motor.set_motor("forward", 50)
    else:
        raise ValueError("Invalid direction. Use 'right' or 'left'.")

    # Calibrate the time needed to turn 90 degrees based on the distance
    time_to_turn = calibrated_turn_distance / 50  # Assuming 50 is the speed and distance is in distance unit

    sleep(time_to_turn)

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

    # Move forward after turning
    left_motor.set_motor("forward", 50)
    right_motor.set_motor("forward", 50)

    # Calibrate the time needed to move forward based on the distance
    time_to_move_forward = calibrated_forward_distance / 50  # Assuming 50 is the speed and distance is in some unit

    sleep(time_to_move_forward)

    # Stop the motors after moving forward
    left_motor.off()
    right_motor.off()

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
