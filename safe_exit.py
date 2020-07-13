from __future__ import print_function
from juicebox import *


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.", file=sys.stderr)
    continue_reading = False
    quit()
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()