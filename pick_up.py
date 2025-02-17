from motion import measure_sensors, drive_forward_depot, turn_in_place_depot
from time import sleep


# This function takes the sensors, motors, linear actuator, QR code reader and ultrasound sensor as arguments
# and navigates the robot trhough the pick-up location, picks up the package and returns the destination
# of the package
def pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor):

    # Lower the linear actuator to pick up position
    linear_actuator.set_actuator(-20)

    # Reverse a bit for better alignment helping QR code scanning
    left_motor.set_motor("reverse", 70)
    right_motor.set_motor("reverse", 70)

    # Delay calibrated manually to ensure QR code scanning
    sleep(0.7)  

    # Move forward slowly and scan for QR code
    while True:

        # Adjust alignment
        sensors_state = measure_sensors(*sensors)
        drive_forward_depot(sensors_state, left_motor, right_motor, 40)  # Slow speed (40% power)
        
        # Keep scanning for QR code message
        message = qr_code_reader.read_message()

        # If message is found store it's first character as destination and break the loop
        if message:
            destination = message[0]
            break
    
    # Continue moving forward slowly and scan distance
    while True:
        sensors_state = measure_sensors(*sensors)
        drive_forward_depot(sensors_state, left_motor, right_motor, 50)  # Slow speed (50% power)

        # Convert sensor readings to a binary mapping
        sensor_state_binary = ''.join(map(str, sensors_state))
            
        # Check for cross-road detection i.e. lines separating the packages in depot
        if sensor_state_binary in ['0111', '1110', '1111']:
            left_motor.set_motor("forward", 50)
            right_motor.set_motor("forward", 50)
            sleep(0.3)                                                  # time to pass the separation lines
        
        # Keep scanning for distance
        distance = ultrasound_sensor.read_distance()

        # If distance is under 5cm or flips completely due to being too close (appearing as 500cm) overshot to ensure proper package pick-up
        if distance > 500 or distance < 5:
            sleep(0.4)                                                  # time to align box

            # Stop the motors after aligning
            left_motor.off()
            right_motor.off()

            # Pick up the package by raising the linear actuator
            linear_actuator.set_actuator(20)  
            break

    # After picking up the package turn in place 180 degrees to the right to leave the depot
    turn_in_place_depot('right', left_motor, right_motor)

    # Reverse a bit to ensure proper alignment for leaving the depot
    left_motor.set_motor("reverse", 70)
    right_motor.set_motor("reverse", 70)
    sleep(0.8)
    left_motor.off()
    right_motor.off()

    # Return the destination of the package from the QR code scan
    return destination
