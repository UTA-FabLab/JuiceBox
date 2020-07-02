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
    #the constructor for the initialization
    def __init__(self):
        self.rid_1 = ""
        self.rid_2 = ""
        self.temp_rid = ""
        self.role_1 = 0
        self.role_2 = 0
        self.trans_id = ""
        self.go = False

    def check_status_operator(self, type, id):
        
        try:
            payload = {"type": type, "number": id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            r.raise_for_status()
            print(response, file=sys.stderr)

        except Exception :
            response = "Check Status: Unable to connect. Verify connection."
        
        return response
    
        try:
            role_json = json.loads(json.dumps(role_info))
            print("Operator Level:",
                role_json["role"], file=sys.stderr)
            

        except Exception:
            print("JSON: ID_1 parse failure", file=sys.stderr)
    
    def check_status_staff(self, type, id):
            
            try:
                payload = {"type": type, "number": id}
                r = requests.request(
                    "POST", serverURL, json=payload, headers=headers)
                response = r.json()
                r.raise_for_status()
                print(response, file=sys.stderr)

            except Exception :
                response = "Check Status: Unable to connect. Verify connection."
                
            return response
            
            role_json_2 = json.loads(json.dumps(role_info_2))
            print("Staff Level:",
                role_json_2["role"], file=sys.stderr)
        
    def authorization_double(self, id_type, id_number, id_number_2, device_id):
        try:
            payload = {"type": id_type, "number": id_number,
                       "number_employee": id_number_2, "device": device_id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
        except ConnectionError as e:
            response =e+": Improper pair of RFID values entered, or Unable to connect."
            print(response, file=sys.stderr)
            self.heart_beat()
            return response
        except HTTPError as e:
            response = e+ ": Request to HTTP server returned unsuccessful status code during RFID authorization phase."
            print(response, file=sys.stderr)
            self.heart_beat()
            return response
        except Exception as e:
            response = e+": This exception in Juicebox.authorization_double() lacks error handling. Codebase is incomplete."
            print(response, file=sys.stderr)
            self.heart_beat()
            return response
        

        return response
#end of Juicebox class

# new subclass for the GPIO pins

class JuiceboxSubclass(Juicebox): 
    
    def end_trans(self,trans_number):
        GPIO.output(pin_connect, True)
        GPIO.output(pin_led_ring, True)
        time.sleep(0.5)
        GPIO.wait_for_edge(pin_button, GPIO.FALLING)
        payload = {"type": "end_transaction", "trans_id": trans_number}
        
        try:
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            print(response)
        except Exception:
            response = "could not end transaction"
            print(response, file=sys.stderr)

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
#end of subclass

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

#main function

def main():
    GPIO.add_event_detect(pin_button, GPIO.FALLING)
    juicebox = Juicebox()
    juiceboxsubclass = JuiceboxSubclass()
    while continue_reading:
        juicebox.go = False
        if (GPIO.event_detected(pin_button)):

                (status, TagType) = MIFAREReader.MFRC522_Request(
                MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    juiceboxsubclass.heart_beat()
                    juicebox.temp_rid = str(
                            uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    print("Operator RFID:", juicebox.temp_rid, file=sys.stderr)
                    rid_1 = juicebox.temp_rid
                    role_info = juicebox.check_status_operator(
                    "check_status_rfid", juicebox.temp_rid)
                    juicebox.go = True
                    #operator info is correct then check for staff
                while juicebox.go == True:
                    (status, TagType) = MIFAREReader.MFRC522_Request(
                        MIFAREReader.PICC_REQIDL)
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        juiceboxsubclass.heart_beat()
                        juicebox.temp_rid = str(uid[0]) + str(uid[1]) + \
                            str(uid[2]) + str(uid[3])
                        print("Staff RFID:", juicebox.temp_rid, file=sys.stderr)
                        rid_2 = juicebox.temp_rid
                        role_info_2 = juicebox.check_status_staff(
                            "check_status_rfid", rid_2)
                        json_obj = juicebox.authorization_double(
                            "rfid_double", rid_1, rid_2, device_id)
                        print("Status:", json_obj, file=sys.stderr)
                        try:
                            if json_obj[u'authorized'] == "Y":
                                trans_id = json_obj[u'trans_id']
                                time.sleep(0.5)
                                
                                end_obj = juiceboxsubclass.end_trans(trans_id)
                                print("End Transaction:",
                                      end_obj, file=sys.stderr)
                                juiceboxsubclass.refresh()
                                break
                            else:
                                juiceboxsubclass.heart_beat()
                                juiceboxsubclass.refresh()
                                break
                        except Exception:
                            print(
                                "Error parsing json of the authorization ... check to make sure the server is returning json.", file=sys.stderr)
                            juiceboxsubclass.refresh()
                            break
        
                        

        time.sleep(0.1)


if __name__ == '__main__':
    main()
