import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
from subprocess import call
import daemon
import lockfile
import signal

TEN_MINUTES = 600000
ONE_MINUTE = 60

def shutdown(signum, frame):  # signum and frame are mandatory
  GPIO.cleanup()
  sys.exit(0)

def main():
  try:
    while True:
      channel = GPIO.wait_for_edge(27, GPIO.RISING, timeout=TEN_MINUTES)
      if channel is None:
        call(["/usr/bin/vcgencmd", "display_power", "0"])
      else:
        call(["/usr/bin/vcgencmd", "display_power", "1"])
        sleep(ONE_MINUTE)

  finally:
    shutdown('', '')

with daemon.DaemonContext(
  pidfile=lockfile.FileLock('/tmp/screen_on_off.pid'),
  signal_map={
    signal.SIGINT: shutdown,
    signal.SIGKILL: shutdown,
    signal.SIGTERM: shutdown,
    signal.SIGTSTP: shutdown
  }):
  main()
