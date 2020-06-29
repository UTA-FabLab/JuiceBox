#!/usr/bin/python2.7

from __future__ import print_function

import httplib
import json
import logging
import signal
import sys
import time

import RPi.GPIO as GPIO
import requests

import MFRC522

# Debug logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

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
GPIO.output(pin_led_ring, False)

headers = {'authorization': "FLUD_KEY"}


class Juicebox:
    #the constructor
    def __init__(self):
        self.rid_1 = ""
        self.rid_2 = ""
        self.temp_rid = ""
        self.role_1 = 0
        self.role_2 = 0
        self.trans_id = ""
        self.go = False

    def check_status(self, type, id):
        
       
        try:
            payload = {"type": type, "number": id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            r.raise_for_status()
            print(response, file=sys.stderr)

        except Exception:
            response = "Check Status: Unable to connect. Verify connection."
            print(response, file=sys.stderr)

        return response

    def authorization_double(self, id_type, id_number, id_number_2, device_id):
        try:
            payload = {"type": id_type, "number": id_number,
                       "number_employee": id_number_2, "device": device_id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()

        except Exception:
            response = "failed to request authorization of 2 different IDs from server.... check connection and url"
            print(response, file=sys.stderr)

        return response

    def end_trans(self, device_id):
        GPIO.output(pin_connect, True)
        GPIO.output(pin_led_ring, True)
        time.sleep(0.5)
        GPIO.wait_for_edge(pin_button, GPIO.FALLING)
        payload = {"type": "end_transaction", "dev_id": device_id}
        try:
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()

        except Exception:
            response = "could not end transaction"
            print(response, file=sys.stderr)
        else:
            print("End Transaction:",end_obj, file=sys.stderr)
        
        GPIO.output(pin_connect, False)
        GPIO.output(pin_led_ring, False)
        
        return response
        
    def heart_beat(self):
        global pin_led_ring
        time.sleep(0.5)
        GPIO.output(pin_led_ring, True)
        time.sleep(0.25)
        GPIO.output(pin_led_ring, False)
        time.sleep(0.25)
        GPIO.output(pin_led_ring, True)
        time.sleep(0.25)
        GPIO.output(pin_led_ring, False)
    
    def refresh(self):
        self.go = False

#end of Juicebox class
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

'''temp_rid = ""
rid_1 = ""
rid_2 = ""
role_1 = 0
role_2 = 0
trans_id = "";
go = True
'''


def main():
    GPIO.add_event_detect(pin_button, GPIO.FALLING)
    juicebox = Juicebox()
    while continue_reading:
        juicebox.go = False
        if (GPIO.event_detected(pin_button)):

                (status, TagType) = MIFAREReader.MFRC522_Request(
                MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    juicebox.heart_beat()
                    juicebox.temp_rid = str(
                            uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    print("Operator RFID:", juicebox.temp_rid, file=sys.stderr)
                    rid_1 = juicebox.temp_rid
                    role_info = juicebox.check_status(
                    "check_status_rfid", juicebox.temp_rid)
                    
                    

                    
                    try:
                        role_json = json.loads(json.dumps(role_info))
                        print("Operator Level:",
                            role_json["role"], file=sys.stderr)
                        juicebox.go = True

                    except Exception:
                        print("JSON: ID_1 parse failure", file=sys.stderr)
                    

                while juicebox.go == True:
                    (status, TagType) = MIFAREReader.MFRC522_Request(
                        MIFAREReader.PICC_REQIDL)
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        juicebox.heart_beat()
                        juicebox.temp_rid = str(uid[0]) + str(uid[1]) + \
                            str(uid[2]) + str(uid[3])
                        print("Staff RFID:", juicebox.temp_rid, file=sys.stderr)
                        rid_2 = juicebox.temp_rid
                        role_info_2 = juicebox.check_status(
                            "check_status_rfid", rid_2)
                        role_json_2 = json.loads(json.dumps(role_info_2))
                        print("Staff Level:",
                              role_json_2["role"], file=sys.stderr)
                        json_obj = juicebox.authorization_double(
                            "rfid_double", rid_1, rid_2, device_id)
                        print("Status:", json_obj, file=sys.stderr)
                        try:
                            if json_obj[u'authorized'] == "Y":
                                GPIO.output(pin_connect, True)
                                GPIO.output(pin_led_ring, True)
                                trans_id = json_obj[u'trans_id']
                                time.sleep(0.5)
                                GPIO.wait_for_edge(pin_button, GPIO.FALLING)
                                end_obj = juicebox.end_trans(device_id)
                                juicebox.refresh()
                                break
                            else:
                                juicebox.heart_beat()
                                juicebox.refresh()
                                break
                        except Exception:
                            print(
                                "Error parsing json of the authorization ... check to make sure the server is returning json.", file=sys.stderr)
                            juicebox.refresh()
                            break
        
                        

        time.sleep(0.1)


if __name__ == '__main__':
    main()
