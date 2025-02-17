from motion import measure_sensors, drive_forward, turn_in_place
from time import sleep

def drop_off(sensors, left_motor, right_motor, linear_actuator, leaving_direction, reverse_time):
    # Move forward until the first cross-road
    while True:
        sensors_state = measure_sensors(*sensors)
        drive_forward(sensors_state, left_motor, right_motor,80)
        
        # Convert sensor readings to a binary string
        sensor_state_binary = ''.join(map(str, sensors_state))
        
        # Check for cross-road detection and drop off the package
        if sensor_state_binary in ['1111','0111','1110']:
            left_motor.off()
            right_motor.off()
            linear_actuator.set_actuator(-20)
            break
    
    # Reverse a set distance and turn towards leaving direction (both depend on which destination AGV is currently at)
    left_motor.set_motor("reverse", 70)
    right_motor.set_motor("reverse", 70)
    sleep(reverse_time)
    left_motor.off()
    right_motor.off()
    turn_in_place(leaving_direction, sensors, left_motor, right_motor)