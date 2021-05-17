"""sleeplapse.py -- a way over complicated time-lapse sleep camera

The original idea was to have a button that allowed me to start/stop the timelapse
and an LED that would blink a few times to show if the button press had just been
accepted.

I scrapped that plan, mostly in order to get a working project faster. :)

I also was thinking I'd cycle the IR LEDs on/off for each picture. However, since
we're taking a picture every 12 seconds or so, I just wired the IR LEDs directly to
5v power.
"""
import time
from pathlib import Path

import arrow
import picamera


# In the end I want a time lapse with 10 fps, that lasts ~4 minutes. For 8 hours,
# that's about 12 seconds between pics.
WAIT_TIME = 6
START_TIME = "15:03"
END_AFTER_HOURS = 9


def start_time():
    """Return an arrow time object with the start time"""
    (shour, smin) = START_TIME.split(":")
    stime = arrow.now()
    return arrow.Arrow(stime.year, stime.month, stime.day, int(shour), int(smin), tzinfo=stime.tzinfo)


def seconds_until_start(start_time, current_time):
    """Return the number of seconds until start time"""
    difference = start_time - current_time
    return difference.seconds 


def wait_until_start():
    """Wait until the start time"""
    stime = start_time()
    keep_waiting = True
    while keep_waiting:
        now = arrow.now()
        until = seconds_until_start(stime, now)
        if until > 60:
            print(f"it's now {now.format('H:mm')} waiting until {stime.format('H:mm')}, holding 1 minute")
            time.sleep(60)
        elif until > 0:
            print(f"{until} seconds until start...")
            time.sleep(1)
        else:
            print("starting.")
            keep_waiting = False


def main():
    pic_path = Path("/home/pi/sleeplapse_pics")
    if not pic_path.exists():
        print(f"Creating pic dir: {pic_path}")
        pic_path.mkdir(parents=True)

    # Sleep for 5 minutes to give us time to actually get into bed and turn off
    # the lights.
    print("Pausing for 5 minutes...")
    time.sleep(300)

    with picamera.PiCamera() as camera:
        camera.resolution(1920, 1080)  # Full HD resolution
        for filename in camera.capture_continuous(
            "/home/pi/sleeplapse_pics/img{timestamp:%H-%M-%S-%f}.jpg"
        ):
            print(time.localtime())
            time.sleep(WAIT_TIME)


if __name__ == "__main__":
    # main()
    wait_until_start()
