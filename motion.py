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
    sensor_state_binary = ''.join(map(str, sensors_state))
    
    # Define motor actions for each sensor state in a binary map   -  !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
    actions = {
        '0000': ('forward', 0, 'forward', 0), #bad
        '0001': ('forward', 0, 'forward', 0), #bad
        '0010': ('forward', 80, 'forward', 60), #correct to right
        '0011': ('forward', 80, 'forward', 60), #correct to right + possible turn right
        '0100': ('forward', 60, 'forward', 80), #correct to left
        '0101': ('forward', 0, 'forward', 0), #bad
        '0110': ('forward', 80, 'forward', 80), #forward
        '0111': ('forward', 0, 'forward', 0), #possible turn right
        '1000': ('forward', 0, 'forward', 0), #bad
        '1001': ('forward', 0, 'forward', 0), #bad
        '1010': ('forward', 0, 'forward', 0), #bad
        '1011': ('forward', 0, 'forward', 0), #bad
        '1100': ('forward', 60, 'forward', 80), #correct left + possible turn left
        '1101': ('forward', 0, 'forward', 0), #bad
        '1110': ('forward', 0, 'forward', 0), #possible turn left
        '1111': ('forward', 0, 'forward', 0), #possible turn right or left
    }
    
    # Get the action for the current sensor state
    left_action, left_speed, right_action, right_speed = actions[sensor_state_binary]
    
    # Set the motors based on the action
    left_motor.set_motor(left_action, left_speed)
    right_motor.set_motor(right_action, right_speed)

    # action delay
    sleep(0.11)


## This function takes a direction, left motor instance
## and right motor instance as arguments
## and turns the robot in place in the given direction

# def turn_in_place(direction, left_motor, right_motor):
#     # Calibrated distance needed for a 180-degree turn
#     calibrated_distance = 180  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!

#     if direction == "right":
#         left_motor.set_motor("forward", 50)
#         right_motor.set_motor("reverse", 50)
#     elif direction == "left":
#         left_motor.set_motor("reverse", 50)
#         right_motor.set_motor("forward", 50)
#     else:
#         raise ValueError("Invalid direction. Use 'right' or 'left'.")

#     time_to_turn = calibrated_distance / 50  # Assuming 50 is the speed and distance is in distance unit

#     sleep(time_to_turn)

#     # Stop the motors after turning
#     left_motor.off()
#     right_motor.off()

## This function takes a direction, left motor instance, and right motor instance as arguments
## and turns the robot in place in the given direction
## then moves forward a bit after turning

# def move_forward_and_turn(direction, left_motor, right_motor):
#     # Calibrated distance needed for a 90-degree turn
#     calibrated_turn_distance = 2  #!!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
#     # Calibrated distance to move forward after turning
#     calibrated_forward_time = 0.45  #!!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!
#                                     # such that it moves forward a distance from sensors to axis

#     # Move forward first
#     left_motor.set_motor("forward", 50)
#     right_motor.set_motor("forward", 50)
#     sleep(calibrated_forward_time)

#     # Then turn in place
#     if direction == "right":
#         left_motor.set_motor("forward", 65)
#         right_motor.set_motor("reverse", 0)
#     elif direction == "left":
#         left_motor.set_motor("reverse", 0)
#         right_motor.set_motor("forward", 65)
#     else:
#         raise ValueError("Invalid direction. Use 'right' or 'left'.")

#     # Calibrate the time needed to turn 90 degrees based on the distance
#     sleep(calibrated_turn_distance)

#     # Stop the motors after turning
#     left_motor.off()
#     right_motor.off()

def turn_in_place(direction, sensors_state, left_motor, right_motor):
    
    # Turn in place until the sensors read '0110'
    
    if direction == "right":
        left_motor.set_motor("forward", 65)
        right_motor.set_motor("reverse", 0)
    elif direction == "left":
        left_motor.set_motor("reverse", 0)
        right_motor.set_motor("forward", 65)
    else:
        raise ValueError("Invalid direction. Use 'right' or 'left'.")

    while True:
        sensor_state_binary = ''.join(map(str, sensors_state))
        if sensor_state_binary == '0110':
            break
        sleep(0.1)  # Small delay

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

def move_forward_and_turn(direction, sensors_state, left_motor, right_motor):
    calibrated_forward_time = 0.45  # This value should be determined through calibration - !!!THIS NEEDS TO BE ADJUSTED WITH PHYSICAL CALIBRATION!!!

    # Move forward first
    left_motor.set_motor("forward", 50)
    right_motor.set_motor("forward", 50)
    sleep(calibrated_forward_time)

    # Then turn in place until the sensors read '0110'
    if direction == "right":
        left_motor.set_motor("forward", 65)
        right_motor.set_motor("reverse", 0)
    elif direction == "left":
        left_motor.set_motor("reverse", 0)
        right_motor.set_motor("forward", 65)
    else:
        raise ValueError("Invalid direction. Use 'right' or 'left'.")

    while True:
        sensor_state_binary = ''.join(map(str, sensors_state))
        if sensor_state_binary == '0110':
            break
        sleep(0.1)  # Small delay

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()