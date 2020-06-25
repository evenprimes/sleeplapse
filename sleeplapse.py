"""sleeplapse.py -- a way over complicated time-lapse sleep camera"""
import time
import RPi.GPIO as GPIO

from contextlib import contextmanager


@contextmanager
def GPIOContext(*args, **kwds):
    """GPIO context so we can use a with statement

    Limitations:
        - Passes all arguments to .setmode()
        - Doesn't support customize .cleanup() channels
    """
    GPIO.setmode(*args, **kwds)
    try:
        yield
    finally:
        GPIO.cleanup()


@contextmanager
def pwn_context(*args, **kwds):
    """pwm context manager so we can use a with statement"""
    pwm = GPIO.PWM(*args, **kwds)
    try:
        pwm.start(0)
        yield pwm
    finally:
        pwm.stop()
