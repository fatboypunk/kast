#! /usr/bin/python
# -*- coding: utf-8; -*-

# import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
from datetime import datetime, time
import logging
import daemon
import sys
import lockfile
import signal

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(27, GPIO.IN)

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("log.file")
logger.addHandler(handler)

TEN_MINUTES = 60
ONE_MINUTE = 6

def shutdown(signum, frame):
  logger.info('Shutting down, bye bye')
  sys.exit(0)

def main():
  try:
    logger.info("booting")
    while True:
      if is_time_between(time(8,30), time(22, 0)):
        logger.info("turn on ")
        call(["/usr/bin/vcgencmd", "display_power", "1"])

      else:
        logger.info("turn off")
        call(["/usr/bin/vcgencmd", "display_power", "0"])

      sleep(ONE_MINUTE)
  finally:
    shutdown('', '')

def is_time_between(begin_time, end_time):
  # If check time is not given, default to current UTC time
  check_time = datetime.utcnow().time()
  if begin_time < end_time:
    return check_time >= begin_time and check_time <= end_time
  else: # crosses midnight
    return check_time >= begin_time or check_time <= end_time



with daemon.DaemonContext(files_preserve=[handler.stream], working_directory='/Users/marcel/code/kast'):
  logger.info('Starting as a daemon')
  main()
