'''
muster from wokwi.com
'''
# Project objective: Pulse the servo from its min to max position and vice-versa
#
# Hardware and connections used:
#   Servo GND to Raspberry Pi Pico GND
#   Servo V+ to Raspberry Pi Pico 3.3 V
#   Servo PWM pin to GPIO Pin 15
# 
# Programmer: Adrian Josele G. Quional

# modules
from picozero import Servo  # importing Servo class to easily control the servo motor
from time import sleep

# creating a Servo object
servo = Servo(15)

# continuously pulse the servo arm from min to max position (and vice-versa) for a duration of 1 sec
while True:
    servo.pulse()
    sleep(1)

'''
muster from wokwi.com
'''

import RPi.GPIO as GPIO
import time
import requests

# ThingSpeak API endpoint and API key
CHANNEL_ID = '2325747'
API_KEY = 'N4H2PP04GTDRHKPZ'

# Ultrasonic sensor pins
TRIGGER_PIN = 18
ECHO_PIN = 19

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Trigger the ultrasonic sensor
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    # Measure the time it takes for the echo to return
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)

try:
    while True:
        distance = measure_distance()
        print(f'Distance: {distance} cm')

        # Send data to ThingSpeak
        params = {'api_key': API_KEY, 'field1': distance}
        response = requests.get(THING_SPEAK_URL, params=params)
        print(f'ThingSpeak Response: {response.status_code}')
        
        time.sleep(15)  # Send data every 15 seconds

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
