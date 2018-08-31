#!/usr/bin/python2.7

from __future__ import print_function
import json
import signal
import time
import sys

import RPi.GPIO as GPIO
import requests

import MFRC522

pin_button = 40
pin_green = 7
pin_red = 8
pin_connect = 3
pin_led_ring = 33

device_id = "DEV_ID"
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_connect, GPIO.OUT)
serverURL = "FLUD_BASE/juicebox.php"
GPIO.output(pin_connect, False)
GPIO.setup(pin_led_ring, GPIO.OUT)

headers = {'authorization': "FLUD_KEY"}


def check_status(type, id):
    try:
        payload = {"type": type, "number": id}
        r = requests.request("POST", serverURL, json=payload, headers=headers)
        response = r.json()
        r.raise_for_status()
        print(response, file=sys.stderr)

    except Exception:
        response = "Check Status: Unable to connect. Verify connection."
        print(response, file=sys.stderr)

    return response


def authorization_double(id_type, id_number, id_number_2, device_id):
    try:
        payload = {"type": id_type, "number": id_number, "number_employee": id_number_2, "device": device_id}
        r = requests.request("POST", serverURL, json=payload, headers=headers)
        response = r.json()

    except Exception:
        response = "failed to request authorization of 2 different IDs from server.... check connection and url"
        print(response, file=sys.stderr)

    return response


def end_trans(number):
    payload = {"type": "end_transaction", "dev_id": number}
    try:
        r = requests.request("POST", serverURL, json=payload, headers=headers)
        response = r.json()

    except Exception:
        response = "could not end transaction"
        print(response, file=sys.stderr)

    return response


def heart_beat():
    global pin_led_ring
    time.sleep(0.5)
    GPIO.output(pin_led_ring, True)
    time.sleep(0.25)
    GPIO.output(pin_led_ring, False)
    time.sleep(0.25)
    GPIO.output(pin_led_ring, True)
    time.sleep(0.25)
    GPIO.output(pin_led_ring, False)


# this is from the MFC library, it is to ensure safe exit
continue_reading = True


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.", file=sys.stderr)
    continue_reading = False
    quit()
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

temp_rid = ""
rid_1 = ""
rid_2 = ""
role_1 = 0
role_2 = 0
trans_id = "";
go = True


def main():
    GPIO.add_event_detect(pin_button, GPIO.FALLING)

    while continue_reading:
        go = True
        if (GPIO.event_detected(pin_button)):

            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                heart_beat()
                temp_rid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                print("Operator RFID:", temp_rid, file=sys.stderr)

                role_info = check_status("check_status_rfid", temp_rid)
                rid_1 = temp_rid
                try:
                    role_json = json.loads(json.dumps(role_info))
                    print("Operator Level:", role_json["role"], file=sys.stderr)

                except Exception:
                    print("JSON: ID_1 parse failure", file=sys.stderr)
                    go = False

                while go == True:
                    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        heart_beat()
                        temp_rid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                        print("Staff RFID:", temp_rid, file=sys.stderr)
                        rid_2 = temp_rid
                        role_info_2 = check_status("check_status_rfid", rid_2)
                        role_json_2 = json.loads(json.dumps(role_info_2))
                        print("Staff Level:", role_json_2["role"], file=sys.stderr)
                        json_obj = authorization_double("rfid_double", rid_1, rid_2, device_id)
                        print("Status:",json_obj, file=sys.stderr)
                        try:
                            if json_obj[u'authorized'] == "Y":
                                GPIO.output(pin_connect, True)
                                GPIO.output(pin_led_ring, True)
                                trans_id = json_obj[u'trans_id']
                                time.sleep(0.5)
                                GPIO.wait_for_edge(pin_button, GPIO.FALLING)
                                end_obj=end_trans(device_id)
                                print("End Transaction:", end_obj, file=sys.stderr)
                                GPIO.output(pin_connect, False)
                                GPIO.output(pin_led_ring, False)
                                break
                            else:
                                heart_beat()
                                break
                        except Exception:
                            print("Error parsing json of the authorization ... check to make sure the server is returning json.", file=sys.stderr)
                            break

        time.sleep(0.1)

if __name__ == '__main__':
    main()
