import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module

relay1_pin = 36
#relay2_pin = 3'



GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
#GPIO.setup(relay2_pin, GPIO.OUT, initial=GPIO.HIGH)   # Set pin relaypin to be an output pin and set initial value to low (off)

def control_camera(cmaera_id, command):
    GPIO.setup(relay1_pin, GPIO.OUT, initial=GPIO.HIGH) 
    print(command)
    if command == 'off':
        GPIO.output(relay1_pin, GPIO.LOW)
        return 'off'
    if command == 'on':
        GPIO.output(relay1_pin, GPIO.HIGH) 
        return 'on'