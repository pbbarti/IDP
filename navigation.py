from motion import measure_sensors, drive_forward, move_forward_and_turn
from time import sleep

# This function takes a list of directions, motor instances
# and array of sensor instances and navigates
# the robot along the path defined by the directions at each consecutive cross-road

def navigate(directions, left_motor, right_motor, sensors):

    # Iterate over the directions
    for direction in directions:

        # Move forward until the next cross-road
        while True:
            sensors_state = measure_sensors(*sensors)
            drive_forward(sensors_state, left_motor, right_motor,90)
            
            # Convert sensor readings to a binary mapping string
            sensor_state_binary = ''.join(map(str, sensors_state))
            
            # Check for cross-road detection
            if sensor_state_binary in ['0111','1110','1111','1010','0101']:             # cross-road cases
                
                # Move forward slightly to pass the cross-road
                if direction == 'straight':
                    left_motor.set_motor("forward", 100)
                    right_motor.set_motor("forward", 100)
                    sleep(0.3)   
                    left_motor.off()
                    right_motor.off()                                                       # time to pass the cross-road
                
                # Turn in the direction specified by the route using the move_forward_and_turn subroutine
                elif direction == 'left':
                    move_forward_and_turn('left', sensors, left_motor, right_motor)
                elif direction == 'right':
                    move_forward_and_turn('right', sensors, left_motor, right_motor)
                
                # Move to the next direction in the directions array
                break


# All relevant routes listed as dictionary

routes = {
    'start_to_depot_1': ['right','right'],
    'depot_1_to_start': ['left','left','straight'],
    'depot_1_to_depot_2': ['left','straight','straight','left'],
    'depot_1_to_A': ['left','straight', 'right'],
    'A_to_depot_1': ['straight', 'right'],
    'depot_1_to_B': ['straight','left','left'],
    'B_to_depot_1': ['right','straight'],
    'depot_1_to_C': ['straight','left','straight','right','left'],
    'C_to_depot_1': ['left','straight','right','straight'],
    'depot_1_to_D': ['straight','straight','left','left'],
    'D_to_depot_1': ['right','straight','straight'],
    'depot_2_to_A': ['right','left'],
    'A_to_depot_2': ['right','right'],
    'depot_2_to_B': ['straight', 'right', 'straight', 'right'],
    'B_to_depot_2': ['left', 'straight', 'left', 'straight'],
    'depot_2_to_C': ['straight', 'right', 'left', 'left'],
    'C_to_depot_2': ['right', 'right', 'left', 'straight'],
    'depot_2_to_D': ['straight', 'straight', 'right', 'straight', 'right'],
    'D_to_depot_2': ['left', 'straight', 'left', 'straight', 'straight'],
    'depot_2_to_start': ['right','straight','right','straight']
}

# Function that outputs direction of turn after drop off
# and reversing time needed depending on the package destination
# calibrated manually

def leave_depot(qr_message):
    if qr_message == "A":
        return ["right", 1.7]
    elif qr_message == "B":
        return ["left", 1]
    elif qr_message == "C":
        return ["left", 1.4]
    elif qr_message == "D":
        return ["left", 1.2]

# Function to choose the route based on QR code message

def choose_route(qr_message):
    if qr_message == "A":
        return routes["depot_1_to_A"], routes["A_to_depot_1"]
    elif qr_message == "B":
        return routes["depot_1_to_B"], routes["B_to_depot_1"]
    elif qr_message == "C":
        return routes["depot_1_to_C"], routes["C_to_depot_1"]
    elif qr_message == "D":
        return routes["depot_1_to_D"], routes["D_to_depot_1"]