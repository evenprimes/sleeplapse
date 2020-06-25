"""
Started with this tutorial.
https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/all#experiment-1-digital-input-and-output
"""
import time
import RPi.GPIO as GPIO

# Pins definitions
btn_pin = 4
IR_PIN = 12
LED_PIN = 13

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(IR_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

is_button_pressed = False
blink_light = False

# If button is pushed, light up LED
try:
    pwm = GPIO.PWM(LED_PIN, 50)
    pwm.start(0)

    for level in range(100, 0, -1):
        pwm.ChangeDutyCycle(level)
        time.sleep(0.02)
    pwm.stop()

    while True:
        if GPIO.input(btn_pin):
            GPIO.output(IR_PIN, GPIO.LOW)
            is_button_pressed = False
        else:
            GPIO.output(IR_PIN, GPIO.HIGH)
            if not is_button_pressed:
                is_button_pressed = True
                print("button pressed")
                print(time.time())


# When you press ctrl+c, this will be called
finally:

    GPIO.cleanup()
