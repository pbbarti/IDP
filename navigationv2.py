from motion import measure_sensors, drive_forward, move_forward_and_turn
from time import sleep
from sensors import QRCodeReader

# Define the routes
routes = {
    "start_to_depot_1": ['straight','right','right'],
    "depot_1_to_depot_2": ['left','straight','straight','left'],
    "depot_1_to_A": ['left','straight', 'right'],
    "A_to_depot_1": ['left','straight', 'right'],
    "depot_1_to_B": ['straight','left','left'],
    "B_to_depot_1": ['right','right','straight'],
    "depot_1_to_C": ['straight','left','straight','right','left'],
    "C_to_depot_1": ['right','left','straight','right','straight'],
    "depot_1_to_D": ['straight','straight','left','left'],
    "D_to_depot_1": ['right','right','straight','straight'],
    "depot_2_to_A": ['right','left'],
    "A_to_depot_2": ['right','right'],
    "depot_2_to_B": ['straight', 'right', 'straight', 'right'],
    "B_to_depot_2": ['left', 'straight', 'left', 'straight'],
    "depot_2_to_C": ['straight', 'right', 'left', 'left'],
    "C_to_depot_2": ['right', 'right', 'left', 'straight'],
    "depot_2_to_D": ['straight', 'straight', 'right', 'straight', 'right'],
    "D_to_depot_2": ['left', 'straight', 'left', 'straight', 'straight'],
    "depot_2_to_start": ['right','straight','right','straight']
}

# direction to turn once drop off depending on the package destination
def leave_depot(qr_message):
    if qr_message == "A":
        return ["right", 2]
    elif qr_message == "B":
        return ["left", 2]
    elif qr_message == "C":
        return ["right", 2]
    elif qr_message == "D":
        return ["left", 2]

# choose the route based on QR code message
def choose_route(qr_message):
    if qr_message == "A":
        return routes["depot_1_to_A"], routes["A_to_depot_1"]
    elif qr_message == "B":
        return routes["depot_1_to_B"], routes["B_to_depot_1"]
    elif qr_message == "C":
        return routes["depot_1_to_C"], routes["C_to_depot_1"]
    elif qr_message == "D":
        return routes["depot_1_to_D"], routes["D_to_depot_1"]
    else:
        return [], []

# Function to navigate the robot through the maze
def navigate(directions, left_motor, right_motor, sensors):
    for direction in directions:
        while True:
            sensors_state = measure_sensors(*sensors)
            drive_forward(sensors_state, left_motor, right_motor, 80)
            
            # Convert sensor readings to a binary string
            sensor_state_binary = ''.join(map(str, sensors_state))
            
            # Check for cross-road detection
            if sensor_state_binary in ['0111', '1110', '1111']:
                left_motor.off()
                right_motor.off()
                
                if direction == 'straight':
                    # Move forward slightly to pass the cross-road
                    left_motor.set_motor("forward", 50)
                    right_motor.set_motor("forward", 50)
                    sleep(0.6)  # Adjust this value based on calibration
                    left_motor.off()
                    right_motor.off()
                elif direction == 'left':
                    move_forward_and_turn('left', sensors, left_motor, right_motor)
                elif direction == 'right':
                    move_forward_and_turn('right', sensors, left_motor, right_motor)
                
                break  # Move to the next direction in the array

# Example usage
qr_message = QRCodeReader.read()  # This would be obtained from the QR code reader
to_destination, to_depot = choose_route(qr_message)

# example main
while True:
    for i in range(3):
        navigate(to_destination, left_motor, right_motor, sensors)
        drop_off(sensors, left_motor, right_motor, linear_actuator, 'left', 2)
        navigate(to_depot, left_motor, right_motor, sensors)
        turn_in_place(turn_in_place_direction, sensors, left_motor, right_motor)
    

# Assuming left_motor, right_motor, and sensors are defined elsewhere in your code
# navigate(to_destination, left_motor, right_motor, sensors)
# navigate(to_depot, left_motor, right_motor, sensors)