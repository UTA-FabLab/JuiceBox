#!/usr/bin/python3

"""This program consisted of the functions which are used in main.py program to check the authority of the operator and the staff members
"""
from __future__ import print_function
import http.client
import json
import logging
import signal
import sys
import time
import mfrc522
import requests

device_id = "0049"
serverURL = "https://fabapp-dev.uta.edu/api/juicebox.php"
headers = {'authorization': "HDVmyqkZB5vsPQGAKwpLtPPQ8Pauy5DMVWsefcBVsbzv9AQnrJFhyAuqBhLCL9r8AFxtDAgjc7Qjf8bdL9eaAXd7VnejU7DHw"}


class Juicebox:
    """This class represents as the parent class for the JuiceBox

    Attributes
    ----------
    rid_1: str
        RFID number of the operator
    rid_2: str
        RFID number of the staff member
    temp_rid: str
        temporary variable for storing the RFID number
    role_1: int
        assigned the default value of role_1 as 0
    role_2: int
        assigned the default value of role_2 as 0
    trans_id: str
        transaction id used for ending the transaction
    go: bool
        assigned the default value as False

    """

    def __init__(self):
        """the constructor for the initialization with default values"""
        self.rid_1 = ""
        self.rid_2 = ""
        self.temp_rid = ""
        self.role_1 = 0
        self.role_2 = 0
        self.trans_id = ""
        self.go = False

    def check_status_operator(self, type, id):
        """This function is used for checking the status of operator with its type and student/operator id number

        Parameters
        ----------
        type: str
            gets the type of rfid status of the operator
        id: int
            gets the student id number of the operator

        Raises
        ------
        ConnectionError
            If the device is not connected to the internet
        """
        try:
            payload = {"type": type, "number": id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            r.raise_for_status()
            print(response, file=sys.stderr)

        except ConnectionError as e:
            """if the information doesnot match throws an Exception
        """
            response = "Check Status: Unable to connect. Verify connection."
            print(e, response)

        return response

    def check_status_staff(self, type, id):
        """This function is used for checking the status of staff member with its type and student/staff id number

        Parameters
        ----------
        type: str
            gets the type of rfid status of the staff member
        id: int
            gets the student id number of the staff member

        Raises
        ------
        ConnectionError
            If the device is not connected to the internet

        """
        try:
            payload = {"type": type, "number": id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            r.raise_for_status()
            print(response, file=sys.stderr)

        except ConnectionError as e:
            """if the information doesnot match throws an Exception
        """
            response = "Check Status: Unable to connect. Verify connection."
            print(e, response)

        return response

    def authorization_double(self, id_type, id_number, id_number_2, device_id):
        """ This function checks whether the id type, id number and device id is correct

        Parameters
        ----------
        id_type: str
            gets the id type for verification
        id_number: int
            validates the id number for the operator
        id_number_2: int
            validates the id number for the staff
        device_id: int
            validates the device id of the device

        Returns
        -------
            str: json file data is returned

        Raises
        ------
        ValueError
            If the function failed to request authorization of different ID's from server
        """
        try:
            payload = {"type": id_type, "number": id_number,
                       "number_employee": id_number_2, "device": device_id}
            r = requests.request(
                "POST", serverURL, json=payload, headers=headers)
            response = r.json()
            print(response)
        except ValueError as e:
            response = "failed to request authorization of 2 different IDs from server.... check connection and url"
            print(e, response)

        return response
# end of Juicebox class
