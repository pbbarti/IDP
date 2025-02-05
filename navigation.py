from motion import measure_sensors, drive_forward, move_forward_and_turn
from time import sleep

## This function takes a list of directions, motor instances
## and array of sensor  instances and navigates
## the robot through the maze of life (or the maze of the track) 

def navigate(directions, left_motor, right_motor, sensors):
    for direction in directions:
        while True:
            sensors_state = measure_sensors(*sensors)
            drive_forward(sensors_state, left_motor, right_motor,80)
            
            # Convert sensor readings to a binary string
            sensor_state_binary = ''.join(map(str, sensors_state))
            
            # Check for cross-road detection
            if sensor_state_binary in ['0011','0111','1100','1110','1111']:
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


## All relevant paths

## NEEDS ADJUSTING + ADD TIMES FOR REVERSE AT EACH DEPO TO DROP-OFF

## reversal times
# destination D - 4s
# destination C - 4.7s
# destination B - 2.2s
# desitnation A - 4s 

    

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
