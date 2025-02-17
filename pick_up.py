from motion import measure_sensors, drive_forward_depot, turn_in_place_depot
from time import sleep

def pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor):

    linear_actuator.set_actuator(-20)  
    left_motor.set_motor("reverse", 70)
    right_motor.set_motor("reverse", 70)
    sleep(0.7)  # Adjust this value based on calibration

    # Move forward slowly and scan for QR code
    while True:
        #adjust to straight first
        sensors_state = measure_sensors(*sensors)
        drive_forward_depot(sensors_state, left_motor, right_motor, 40)  # Slow speed
         
        sensor_state_binary = ''.join(map(str, sensors_state))
        
        # Scan for QR code message
        message = qr_code_reader.read_message()
        if message:
            destination = message[0]
            break
    
    # Continue moving forward slowly and scan distance
    while True:
        sensors_state = measure_sensors(*sensors)
        drive_forward_depot(sensors_state, left_motor, right_motor, 50)  # Slow speed
        # Convert sensor readings to a binary string
        sensor_state_binary = ''.join(map(str, sensors_state))
            
        # Check for cross-road detection
        if sensor_state_binary in ['0111', '1110', '1111']:
            left_motor.set_motor("forward", 50)
            right_motor.set_motor("forward", 50)
            sleep(0.3)  # Adjust this value based on calibration
        

       
        # Scan for distance
        distance = ultrasound_sensor.read_distance()
        if distance > 500 or distance < 5:
            sleep(0.4)
            left_motor.off()
            right_motor.off()
            linear_actuator.set_actuator(20)  
            break

    # Turn around
    turn_in_place_depot('right', left_motor, right_motor)

    # Reverse a bit
    left_motor.set_motor("reverse", 70)
    right_motor.set_motor("reverse", 70)
    sleep(0.8)

    return destination

# Example usage
# i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))
# qr_code_reader = QRCodeReader(i2c, 0x0C)
# ultrasound_sensor = UltrasoundSensor(pin=26)
# pick_up(sensors, left_motor, right_motor, linear_actuator, qr_code_reader, ultrasound_sensor)



