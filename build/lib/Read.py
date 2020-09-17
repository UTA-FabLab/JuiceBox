#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import signal
import requests

import MFRC522
import RPi.GPIO as GPIO

pin_button = 40
pin_green = 7
pin_red = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
serverURL = "FLUD_BASE/flud.php"


def authorization(id_type, id_number, device_number):
    global serverURL
    r = requests.post(url=serverURL, data=json.dumps({"type": id_type, "number": id_number, "device": device_number}))
    response = r.text
    return response


continue_reading = True


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

while continue_reading:

    #	GPIO.wait_for_edge( pin_button, GPIO.FALLING )

    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
# print authorization( "utaid", "UTA_ID", "0001" )
