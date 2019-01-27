#! /usr/bin/python
# -*- coding: utf-8; -*-
import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
import logging
import daemon
import daemon.pidlockfile
import sys
import lockfile
import signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("log.file")
logger.addHandler(handler)

TEN_MINUTES = 600000
ONE_MINUTE = 60

def shutdown(signum, frame):
  logger.info('Shutting down, bye bye')
  GPIO.cleanup()
  sys.exit(0)

def main():
  try:
    while True:
      logger.info('Starting')
      channel = GPIO.wait_for_edge(27, GPIO.RISING, timeout=TEN_MINUTES)
      if channel is None:
        logger.info('Not heard anything for 10 minutes, power down')
        call(["/usr/bin/vcgencmd", "display_power", "0"])
      else:
        logger.info('Heard something, power on')
        call(["/usr/bin/vcgencmd", "display_power", "1"])
        logger.info('Sleeping')
        sleep(ONE_MINUTE)
        logger.info('Sleeping is over')

  finally:
    shutdown('', '')

with daemon.DaemonContext(
        pidfile=lockfile.FileLock('/var/run/screen_on_off.pid'),
        files_preserve=[handler.stream],
        working_directory='/home/pi/kast'):
  logger.info('Starting as a daemon')
  main()
