from __future__ import print_function
import httplib
import json
import logging
import signal
import sys
import time

import requests
import MFRC522

device_id = "DEV_ID"
serverURL = "FLUD_BASE/juicebox.php"
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

                          
    def authorization_double(self, id_type, id_number, id_number_2, device_id):
        try:
            payload = {"type": id_type, "number": id_number,
                       "number_employee": id_number_2, "device": device_id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            print(response)
        except ValueError as e:
            response = "failed to request authorization of 2 different IDs from server.... check connection and url"
            print(e,response)

        return response
#end of Juicebox class