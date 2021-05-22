"""sleeplapse.py -- a way over complicated time-lapse sleep camera

The original idea was to have a button that allowed me to start/stop the timelapse
and an LED that would blink a few times to show if the button press had just been
accepted.

I scrapped that plan, mostly in order to get a working project faster. :)

I also was thinking I'd cycle the IR LEDs on/off for each picture. However, since
we're taking a picture every 12 seconds or so, I just wired the IR LEDs directly to
5v power.
"""
import logging
import logging.handlers
import os
import sys
import time
from pathlib import Path

import arrow
import picamera


# In the end I want a time lapse with 10 fps, that lasts ~4 minutes. For 8 hours,
# that's about 12 seconds between pics.
WAIT_TIME = 6
START_TIME = "23:30"        # 11:30 PM
END_AFTER_HOURS = 9         # Stop after 9 hours, since we're getting up at 8


# Setup our basic logging options
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/sleeplapse/lapse.log"))
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
handler.setFormatter(formatter)
log = logging.getLogger("sleeplapselogging")
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
log.addHandler(handler)
log.info("Hello, world")


def start_and_end_time():
    """Return an arrow time object with the start time"""
    (shour, smin) = START_TIME.split(":")
    stime = arrow.now()
    start_time = arrow.Arrow(stime.year, stime.month, stime.day, int(shour), int(smin), tzinfo=stime.tzinfo)
    if stime > start_time:
        # If start time is in the past, start now
        start_time = stime
    if __debug__:
        end_time = start_time.shift(minutes=+2)
    else:
        end_time = start_time.shift(hours=+END_AFTER_HOURS)
    return start_time, end_time


def seconds_until_start(start_time, current_time):
    """Return the number of seconds until start time"""
    difference = start_time - current_time
    return difference.seconds


def wait_until_start(start_time):
    """Wait until the start time

    This just ses the time.sleep() call. I could get slick and just sleep 1 time for a much longer period, but
    I want to be able to review the log file and verify that things are running.
    """
    # stime = start_time()
    if arrow.now() > start_time:
        log.info("Starting immediately")
        return
    keep_waiting = True
    while keep_waiting:
        now = arrow.now()
        until = seconds_until_start(start_time, now)
        if until > 60:
            log.info(f"it's now {now.format('H:mm')} waiting until {start_time.format('H:mm')}, holding 1 minute")
            time.sleep(60)
        elif until > 0:
            log.info(f"{until} seconds until start...")
            time.sleep(1)
        else:
            log.info("starting.")
            keep_waiting = False


def timelapse():
    """Run the timelapse

    This does the actual timelapse. The big thing here is that the timestamp is used. The files will be renamed
    as part of adding the timestamp onto the images. I use a full date timestamp so that if there's an
    exception that triggers, the program will just pick up again and there won't be any filename/sequence issues
    in the recovery.
    """
    now = arrow.now()
    pic_path = Path(f"/home/pi/lapse_{now.format('YYYY-MM-DD')}")
    if not pic_path.exists():
        log.info(f"Creating pic dir: {pic_path}")
        pic_path.mkdir(parents=True)
    os.chdir(pic_path)
    log.info(f"Picture directory: {pic_path}")

    if __debug__:
        # In __debug__ mode, just run for 3 minutes.
        end_time = now.shift(minutes=+3)
    else:
        end_time = now.shift(hours=+END_AFTER_HOURS)

    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)    # Full HD resolution
        camera.rotation = 90                # The camera is on it's side. /shrug
        for filename in camera.capture_continuous("sl_{timestamp:%Y%j_%H%M%S}.jpg"):
            # Using the timestamp to ensure that there are no collisions when/if there's a problem during
            # the night and the timelapse "restarts"
            log.info(f"Taking pic at: {time.asctime()}")
            if arrow.now() > end_time:
                log.info("Got to end time, quitting normally")
                break
            else:
                time.sleep(WAIT_TIME)


if __name__ == "__main__":
    if __debug__: print("In debug mode")
    log.info("Starting program ===============================")
    start_time, end_time = start_and_end_time()
    log.info(f"Start time: {start_time}")
    log.info(f"End time: {end_time}")
    while arrow.now() < end_time:
        try:
            wait_until_start(start_time)
            timelapse()
            log.info("Ended program normally =========================")
        except:
            log.exception("Something fucked up!!!")
            # sys.exit(1)
