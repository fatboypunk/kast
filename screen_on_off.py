import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
import logging
import daemon
import lockfile
import signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
logging.basicConfig(format='%(asctime)s %(message)s', filename='log.log',level=logging.INFO)
TEN_MINUTES = 600000
ONE_MINUTE = 60

def shutdown(signum, frame):
  logging.info('Shutting down, bye bye')
  GPIO.cleanup()
  sys.exit(0)

# def main():
try:
  while True:
    channel = GPIO.wait_for_edge(27, GPIO.RISING, timeout=TEN_MINUTES)
    if channel is None:
      logging.info('Not heard anything for 10 minutes, power down')
      call(["/usr/bin/vcgencmd", "display_power", "0"])
    else:
      logging.info('Heard something, power on')
      call(["/usr/bin/vcgencmd", "display_power", "1"])
      logging.info('Sleeping')
      sleep(ONE_MINUTE)
      logging.info('Sleeping is over')

finally:
  shutdown('', '')

# with daemon.DaemonContext(
#         pidfile=lockfile.FileLock('/var/run/screen_on_off.pid'),
#         working_directory='/home/pi/kast'):
#   logging.info('Starting as a daemon')
#   main()
