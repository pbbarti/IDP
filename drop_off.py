from motion import measure_sensors, drive_forward, turn_in_place
from time import sleep

def drop_off(sensors, left_motor, right_motor, linear_actuator, leaving_direction, reverse_time):
    # Move forward until the first cross-road
    while True:
        sensors_state = measure_sensors(*sensors)
        drive_forward(sensors_state, left_motor, right_motor,50)
        
        # Convert sensor readings to a binary string
        sensor_state_binary = ''.join(map(str, sensors_state))
        
        # Check for cross-road detection
        if sensor_state_binary in ['1111','0111','1110']:
            
            left_motor.off()
            right_motor.off()
            sleep(0.5) 
            linear_actuator.set_actuator(-30)
            break
    
    # Reverse a set distance
    left_motor.set_motor("reverse", 40)
    right_motor.set_motor("reverse", 40)
    sleep(reverse_time)  # Adjust this value based on calibration
    left_motor.off()
    right_motor.off()
    linear_actuator.set_actuator(30)
    
    turn_in_place(leaving_direction, sensors, left_motor, right_motor)