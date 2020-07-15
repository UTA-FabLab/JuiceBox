#!/usr/bin/python3

#this file consisted of the functions which are used in main file to check the authority 
#of the operator and the staff member

from __future__ import print_function
import http.client
import json
import logging
import signal
import sys
import time

import requests
import mfrc522

device_id = "DEV_ID"                  
serverURL = "FLUD_BASE/juicebox.php"
headers = {'authorization': "FLUD_KEY"}

class Juicebox:
    #the constructor for the initialization with default values
    def __init__(self):
        self.rid_1 = ""
        self.rid_2 = ""
        self.temp_rid = ""
        self.role_1 = 0
        self.role_2 = 0
        self.trans_id = ""
        self.go = False
#function for checking the status of operator with its type and student id
    def check_status_operator(self, type, id):
        
        try:
            payload = {"type": type, "number": id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            r.raise_for_status()
            print(response, file=sys.stderr)
            
#if the information doesnot match throws an Exception
        except Exception :
            response = "Check Status: Unable to connect. Verify connection."
        
        return response
    
 #function for checking the status of the staff member with its type and student/staff id  
    def check_status_staff(self, type, id):
            
            try:
                payload = {"type": type, "number": id}
                r = requests.request(
                    "POST", serverURL, json=payload, headers=headers)
                response = r.json()
                r.raise_for_status()
                print(response, file=sys.stderr)
                
#if the information doesnot match throws an Exception                
            except Exception :
                response = "Check Status: Unable to connect. Verify connection."
               
            return response

#function to check whether the id of operator and staff is correct from the server and also checks the type and the device id                          
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