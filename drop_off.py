from motion import measure_sensors, drive_forward, turn_in_place
from time import sleep

def drop_off(left_motor, right_motor, linear_actuator, sensors):
    # Move forward until the first cross-road
    while True:
        sensors_state = measure_sensors(*sensors)
        drive_forward(sensors_state, left_motor, right_motor)
        
        # Convert sensor readings to a binary string
        sensor_state_binary = ''.join(map(str, sensors_state))
        
        # Check for cross-road detection
        if sensor_state_binary == '1111':
             # Move forward through the cross-road
            left_motor.set_motor("forward", 50)
            right_motor.set_motor("forward", 50)
            sleep(0.5)  # Adjust this value based on calibration
            left_motor.off()
            right_motor.off()
        elif sensor_state_binary == '0000':
            left_motor.off()
            right_motor.off()
            break
    
    sleep(0.5)  # Lag before retracting the linear actuator
    # Fully retract the linear actuator
    linear_actuator.fully_retract()
    
    # Reverse a set distance
    left_motor.set_motor("reverse", 50)
    right_motor.set_motor("reverse", 50)
    sleep(1)  # Adjust this value based on calibration
    left_motor.off()
    right_motor.off()
    # Turn 180 degrees
    turn_in_place('right', sensors_state, left_motor, right_motor)