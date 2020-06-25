# sleeplapse
An over designed sleep timelapse generator for Raspberry Pi.

Goal is to have this running on the RPi all night and then generate a timelapse
in the morning.

While this is normally 5 lines of code, I can't make things that simple. Plus, the
NoIR Camera module needs *something* to get decent pics.

Silly enchancements:
- Use 3 IR LEDs to illuminate the room enough to get a picture
- Use a button to start/stop the picture taking
- Use a regular LED to indicate starting/stopping status (but not all night since
that might keep me up)
