from sensors import LineFollowingSensor
from motors import Motor_Right, Motor_Left
from motion import measure_sensors, drive_forward, move_forward_and_turn, stop_motors
from time import sleep

## This function takes a list of directions and navigates the robot through the maze of life (or the maze of the track)

def navigate(directions, left_motor, right_motor, sensors):
    for direction in directions:
        while True:
            sensor_state = measure_sensors(*sensors)
            drive_forward(sensor_state, left_motor, right_motor)
            
            # Convert sensor readings to a binary string
            sensor_state_str = ''.join(map(str, sensor_state))
            
            # Check for cross-road detection
            if sensor_state_str in ['0011','0111','1100','1110','1111']:
                stop_motors(left_motor, right_motor)
                
                if direction == 'straight':
                    # Move forward slightly to pass the cross-road
                    left_motor.set_motor("forward", 50)
                    right_motor.set_motor("forward", 50)
                    sleep(1)  # Adjust this value based on calibration
                    stop_motors(left_motor, right_motor)
                elif direction == 'left':
                    move_forward_and_turn('left', left_motor, right_motor)
                elif direction == 'right':
                    move_forward_and_turn('right', left_motor, right_motor)
                
                break  # Move to the next direction in the array

# Example usage
#right_motor = Motor_Right(direction_pin=7, speed_pin=6)
#left_motor = Motor_Left(direction_pin=4, speed_pin=5)
#sensors = [
    #LineFollowingSensor(pin=21),
    #LineFollowingSensor(pin=20),
    #LineFollowingSensor(pin=19),
    #LineFollowingSensor(pin=18)
#]

#directions = ['left', 'left', 'straight', 'left', 'left']
#navigate(directions, left_motor, right_motor, sensors)


## All relevant paths

start_to_depot_1 = ['straight','right','right']
depot_1_to_depot_2 = ['left','straight','straight','left']
depot_1_to_A = ['left','straight', 'right']
A_to_depot_1 = ['left','straight', 'right']
depot_1_to_B = ['straight','left','left']
B_to_depot_1 = ['right','right','straight']
depot_1_to_C = ['straight','left','straight','right','left']
C_to_depot_1 = ['right','left','straight','right','straight']
depot_1_to_D = ['straight','straight','left','left']
D_to_depot_1 = ['right','right','straight','straight']
depot_2_to_A = ['right','left']
A_to_depot_2 = ['right','right']
depot_2_to_B = ['straight', 'right', 'straight', 'right']
B_to_depot_2 = ['left', 'straight', 'left', 'straight']
depot_2_to_C = ['straight', 'right', 'left', 'left']
C_to_depot_2 = ['right', 'right', 'left', 'straight']
depot_2_to_D = ['straight', 'straight', 'right', 'straight', 'right']
D_to_depot_2 = ['left', 'straight', 'left', 'straight', 'straight']
depot_2_to_start = ['right','straight','right','straight']
