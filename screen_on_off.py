import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
from subprocess import call

TEN_MINUTES = 600000
ONE_MINUTE = 6

try:
  while True:
    print('waiting')
    channel = GPIO.wait_for_edge(17, GPIO.RISING, timeout=TEN_MINUTES)
    if channel is None:
      print('been quite for 10 min')
      call(["/usr/bin/vcgencmd", "display_power", "0"])
    else:
      print('heard a sound')
      print(dir(channel))
      call(["/usr/bin/vcgencmd", "display_power", "1"])
      sleep(ONE_MINUTE)
      print('stopped_sleeping')

finally:
  GPIO.cleanup()
