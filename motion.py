from time import sleep

# This function takes a list of sensors and returns a list of their values
def measure_sensors(LineFollowingSensor_1, LineFollowingSensor_2, LineFollowingSensor_3, LineFollowingSensor_4 ):
    reading = []
    reading.append(LineFollowingSensor_1.read_value())
    reading.append(LineFollowingSensor_2.read_value())
    reading.append(LineFollowingSensor_3.read_value())
    reading.append(LineFollowingSensor_4.read_value())
    return reading


# This function takes a list of sensors measurements
# two motor instances
# and operating speed as arguments
# and based on the values of sensors measurements
# sets driving parameters for motors to follow the line

def drive_forward(sensors_state, left_motor, right_motor, speed):
    # Convert readings into binary mapping of sensors states
    sensor_state_binary = ''.join(map(str, sensors_state))
    
    # Define motor actions for each sensor state in a binary map
    actions = {
        '0000': ('forward', 0, 'forward', 0),             # dead state
        '0001': ('reverse', speed-20, 'reverse', speed),  # retract with right wheel rotation to correct path
        '0010': ('forward', speed, 'forward', speed-20),  # correct to right
        '0011': ('forward', speed, 'forward', speed-20),  # correct to right
        '0100': ('forward', speed-20, 'forward', speed),  # correct to left
        '0101': ('forward', 0, 'forward', 0),             # dead state
        '0110': ('forward', speed, 'forward', speed),     # keep forward
        '0111': ('forward', 0, 'forward', 0),             # dead state
        '1000': ('reverse', speed, 'reverse', speed -20), # retract with left wheel rotation to correct path
        '1001': ('forward', 0, 'forward', 0),             # dead state
        '1010': ('forward', 0, 'forward', 0),             # dead state
        '1011': ('forward', 0, 'forward', 0),             # dead state
        '1100': ('forward', speed-20, 'forward', speed),  # correct to left
        '1101': ('forward', 0, 'forward', 0),             # dead state
        '1110': ('forward', 0, 'forward', 0),             # dead state
        '1111': ('forward', 0, 'forward', 0),             # dead state
    }
    
    # Get the action for the current sensor state
    left_action, left_speed, right_action, right_speed = actions[sensor_state_binary]
    
    # Set the motors direcetion and speed based on the action necessary
    left_motor.set_motor(left_action, left_speed)
    right_motor.set_motor(right_action, right_speed)

    # Control delay
    sleep(0.08)

# This function operats in a similar way to the drive_forward function
# but it is used for the depot area where the robot needs to be more precise
# and the control policy is more aggressive with reduced speeds in order to
# converge on the line more precisely for pick up

def drive_forward_depot(sensors_state, left_motor, right_motor, speed):
    # Convert readings into binary mapping of sensors states
    sensor_state_binary = ''.join(map(str, sensors_state))
    
    # Define motor actions for each sensor state in a binary map
    actions = {
        '0000': ('forward', 0, 'forward', 0),             # dead state
        '0001': ('reverse', speed-40, 'reverse', speed),  # retract with right wheel rotation to correct path
        '0010': ('forward', speed, 'forward', speed-40),  # correct to right
        '0011': ('forward', speed, 'forward', speed-40),  # correct to right
        '0100': ('forward', speed-40, 'forward', speed),  # correct to left
        '0101': ('forward', 0, 'forward', 0),             # dead state
        '0110': ('forward', speed, 'forward', speed),     # keep forward
        '0111': ('forward', 0, 'forward', 0),             # dead state
        '1000': ('reverse', speed, 'reverse', speed -40), # retract with left wheel rotation to correct path
        '1001': ('forward', 0, 'forward', 0),             # dead state
        '1010': ('forward', 0, 'forward', 0),             # dead state
        '1011': ('forward', 0, 'forward', 0),             # dead state
        '1100': ('forward', speed-40, 'forward', speed),  # correct to left
        '1101': ('forward', 0, 'forward', 0),             # dead state
        '1110': ('forward', 0, 'forward', 0),             # dead state
        '1111': ('forward', 0, 'forward', 0),             # dead state
    }
    
    # Get the action for the current sensor state
    left_action, left_speed, right_action, right_speed = actions[sensor_state_binary]
    
    # Set the motors direcetion and speed based on the action necessary
    left_motor.set_motor(left_action, left_speed)
    right_motor.set_motor(right_action, right_speed)

    # Control delay
    sleep(0.09)


# This function takes a direction, motor instances and sensors as arguments
# and turns the robot in place in the given direction
# until sensors read position corresponing to being on the line

def turn_in_place(direction, sensors, left_motor, right_motor):
    
    # Turn in place until the sensors read postion on the line
    if direction == "right":
        left_motor.set_motor("forward", 70)
        right_motor.set_motor("reverse", 70)
    elif direction == "left":
        left_motor.set_motor("reverse", 70)
        right_motor.set_motor("forward", 70)

    # small delay in order to avoid initial alginment with the line to be confused with turning finish
    sleep(1.1)

    # continue reading sensors until the robot is aligned with the line
    while True:
        sensors_state = measure_sensors(*sensors)
        sensor_state_binary = ''.join(map(str, sensors_state))
        if sensor_state_binary in ['0100','0010','0110']:
            break
        # Control delay
        sleep(0.11)

    # Overshot delay calibrated manually to ensure better alignment
    sleep(0.14)

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

# This function takes a direction, motor instances and sensors as arguments
# and moves the robot forward and turns in the given direction
# using similar control policy as the turn_in_place function

def move_forward_and_turn(direction, sensors, left_motor, right_motor):
    # Forward overshoot delay calibrated manually to ensure propper alignment after turning
    calibrated_forward_time = 0.15

    # Move forward first
    left_motor.set_motor("forward", 100)
    right_motor.set_motor("forward", 100)
    sleep(calibrated_forward_time)

    # Turn in place until the sensors read postion on the line 
    if direction == "right":
        left_motor.set_motor("forward", 100)
        right_motor.set_motor("reverse", 30)
    elif direction == "left":
        left_motor.set_motor("reverse", 30)
        right_motor.set_motor("forward", 100)

    # small delay in order to avoid initial alginment with the line to be confused with turning finish
    sleep(0.7)

    # continue reading sensors until the robot is aligned with the line
    while True:
        sensors_state = measure_sensors(*sensors)
        sensor_state_binary = ''.join(map(str, sensors_state))
        if sensor_state_binary in ['0100','0010','0110']:
            break
        # Control delay
        sleep(0.1)

    # Overshot delay calibrated manually to ensure better alignment
    sleep(0.13)

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

# This function takes a direction, motor instances and sensors as arguments
# and turns the robot 180 degrees in place in the given direction 

def turn_in_place_depot(direction, left_motor, right_motor):
    
    # Start turning in place
    if direction == "right":
        left_motor.set_motor("forward", 70)
        right_motor.set_motor("reverse", 70)
    elif direction == "left":
        left_motor.set_motor("reverse", 70)
        right_motor.set_motor("forward", 70)

    # Delay calibrated manually to ensure 180 degree turn
    sleep(2.4)

    # Stop the motors after turning
    left_motor.off()
    right_motor.off()

# This function takes motor instances and sensors as arguments
# and moves the robot forward until the first cross-road indicating the end of the starting area

def start_area(left_motor, right_motor, sensors):
    
    # Move forward until the first cross-road indicating the end of the starting area
     while True:
            sensors_state = measure_sensors(*sensors)
            left_motor.set_motor("forward", 100)
            right_motor.set_motor("forward", 100)

            # Convert sensor readings to binary mapping
            sensor_state_binary = ''.join(map(str, sensors_state))
            
            # Check for cross-road detection
            if sensor_state_binary in ['0111','1110','1111']:
                
                # Overshot delay to pass the cross-road
                sleep(0.2)

                # Stop the motors after passing
                left_motor.off()
                right_motor.off()
                break

# This function takes motor instances as arguments
# and moves the robot forward with overshoot delay to finish inside the starting area  

def start_area_finish(left_motor, right_motor):
        left_motor.set_motor('forward',70)
        right_motor.set_motor('forward',70)

        # Overshot delay to finish inside the starting area
        sleep(1)

        # Stop the motors after passing
        left_motor.off()
        right_motor.off()
