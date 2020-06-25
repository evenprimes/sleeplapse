import time
import RPi.GPIO as GPIO
from pygame import mixer

# Pins definitions
btn_pin = 4
IR_PIN = 12
LED_PIN = 13

# Set up pins
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(btn_pin, GPIO.IN)
# GPIO.setup(LED_PIN, GPIO.OUT)

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(IR_PIN, GPIO.OUT)

# Initialize pygame mixer
mixer.init()

# Remember the current and previous button states
current_state = True
prev_state = True

# Load the sounds
sound = mixer.Sound("applause-1.wav")

# If button is pushed, light up LED
try:
    while True:
        current_state = GPIO.input(btn_pin)
        print(current_state)
        if (current_state == False) and (prev_state == True):
            if mixer.get_busy():
                mixer.stop()
            sound.play()
            GPIO.output(IR_PIN, GPIO.HIGH)
        if not mixer.get_busy():
            GPIO.output(IR_PIN, GPIO.LOW)
        prev_state = current_state


# When you press ctrl+c, this will be called
finally:
    mixer.quit()
    GPIO.cleanup()
