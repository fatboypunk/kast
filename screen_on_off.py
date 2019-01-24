import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 15)
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
GPIO.setup(17, GPIO.IN)    # set GPIO17 as input (button)
from subprocess import call
from datetime import datetime, timedelta

TEN_MINUTES = 60000

try:
  while True:
    channel = GPIO.wait_for_edge(17, GPIO.RISING, timeout=TEN_MINUTES)
    if channel is None:
      call(["/usr/bin/vcgencmd", "display_power", "0"])
    else:
      call(["/usr/bin/vcgencmd", "display_power", "1"])
finally:                   # this block will run no matter how the try block exits
  GPIO.cleanup()         # clean up after yourself
