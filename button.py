"""
Started with this tutorial.
https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/all#experiment-1-digital-input-and-output
"""
import time
import RPi.GPIO as GPIO

# Pins definitions
btn_pin = 4
led_pin = 12

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

is_button_pressed = False
blink_light = False

# If button is pushed, light up LED
try:
    while True:
        if GPIO.input(btn_pin):
            GPIO.output(led_pin, GPIO.LOW)
            is_button_pressed = False
        else:
            GPIO.output(led_pin, GPIO.HIGH)
            if not is_button_pressed:
                is_button_pressed = True
                print("button pressed")
                print(time.time())


# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
