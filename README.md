# sleeplapse

An over designed sleep timelapse generator for Raspberry Pi.

Goal is to have this running on the RPi all night and then generate a timelapse
in the morning.

I've got 8 IR LEDs wired directly to 5v power, so no need to control them in
code.

## Python packages

I used `apt-get` to install `python3-picamera`. That's the only extra package
needed.
