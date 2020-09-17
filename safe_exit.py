from __future__ import print_function
from juicebox import *

#ending the reading from file and quitting
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.", file=sys.stderr)
    continue_reading = False
    quit()
    GPIO.cleanup()