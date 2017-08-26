#!/usr/bin/env python
# -*- coding: utf8 -*-

# tessting new pull

import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
import json
import time
import pprint
import urllib, urllib2
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


pin_button = 40
pin_green = 7
pin_red = 8
pin_connect = 3
pin_led_ring = 10



device_id = "DEV_ID"
GPIO.setmode( GPIO.BOARD )
GPIO.setup( pin_button, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.setup( pin_connect, GPIO.OUT )
serverURL = "FLUD_BASE/flud.php"
GPIO.output( pin_connect, False )
GPIO.setup( pin_led_ring, GPIO.OUT )

file_exists = False

while file_exists == False:
	if os.path.exists("/home/pi/config.json"):
		file_exists = True
	else:
		print "no files"

with open("/home/pi/config.json") as json_file:
    json_data = json.load(json_file)
    device_id = json_data[u'config_data'][0][u'device_num']
    serverURL = json_data[u'config_data'][0][u'server_url']

# this is the method that will post data to flud.php, or global serverURL
def authorization(id_type, id_number, device_number):

	global serverURL
	global device_id

	try:
		data = json.dumps( {"type":id_type, "number":id_number, "device":device_number} )
		req = urllib2.Request( serverURL, data )
		print req
		f = urllib2.urlopen( req, context=ctx )
		print f
		response = f.read()

		print "authorization: "
		print response

	except Exception:
		response = "failed to request authorization from server, make sure the connection and url are correct"

	return response



def check_status( type,  id ):

	global serverURL

	try:
		data = json.dumps( { "type":type, "number":id } )
		req = urllib2.Request( serverURL, data )
		f = urllib2.urlopen( req, context=ctx )
		print "checking status"
		response = f.read()
		print response

	except Exception:
		response = "failed to request ID status from server, make sure the connection and url are accurate"

	return response


def authorization_double(id_type, id_number, id_number_2, device_number):

	global serverURL
	global device_id

	try:
		data=json.dumps({ "type":id_type, "number":id_number, "number_employee":id_number_2, "device":device_id })
		req = urllib2.Request( serverURL, data )
		f = urllib2.urlopen( req, context=ctx )
		response = f.read()
		print response
		f.close()

	except Exception:
		response = "failed to request authorization of 2 different IDs from server.... check connection and url"


	return response


# this is the method that will send the poweroff notification to flud.php
def end_trans( type, trans_id, trans_end ):
	global serverURL

	try:
		r = requests.post( url = serverURL, data = json.dumps( { "type":type, "trans_id":trans_id, "trans_end":trans_end } ) )
		response = r.json()
	except Exception:
		response = "failed to close the transaction .... check connection and url, also make sure the response is json"

	return response


def end_trans( number ):
	global serverURL

	data = json.dumps( { "type":"end_transaction", "trans_id":trans_id } )

	try:
		req = urllib2.Request( serverURL, data )
		f = urllib2.urlopen( req, context=ctx )
		response = f.read()
		print response
		f.close()
	except Exception:
		response = "could not end transaction"

	return response


def heart_beat():
	global pin_led_ring
	time.sleep(0.5)
	GPIO.output( pin_led_ring, True )
	time.sleep(0.25)
	GPIO.output( pin_led_ring, False )
	time.sleep(0.25)
	GPIO.output( pin_led_ring, True )
	time.sleep(0.25)
	GPIO.output( pin_led_ring, False )



# this is from the MFC library, it is to ensure safe exit
continue_reading = True
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
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

# MAIN FUNCTION
# while loop waiting for button press then read rfid then

# logic:
#	Read the first RFID card when the button is pressed.
#	send the request to get the role of first RFID and print
#	

# main loop with interrupts....

GPIO.add_event_detect( pin_button, GPIO.FALLING )

while continue_reading:
	go = True
	if( GPIO.event_detected( pin_button ) ):

		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	    	(status,uid) = MIFAREReader.MFRC522_Anticoll()
		if status == MIFAREReader.MI_OK:
			heart_beat()
			temp_rid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])

			role_info = str(check_status("check_status_rfid", temp_rid))
			rid_1 = temp_rid
			print role_info

			try:
				role_json = json.loads( str(role_info) )
				print role_json[u'role']
			except Exception:
				print "error parsing the JSON of the first ID"
				go = False

			while go == True:
				time.sleep(2)
				(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
			    	(status,uid) = MIFAREReader.MFRC522_Anticoll()
				if status == MIFAREReader.MI_OK:
					heart_beat()
					temp_rid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
					rid_2 = temp_rid
					role_info_2 = str( check_status("check_status_rfid", rid_2 ))
					print role_info_2
					#try:
					#	role_2_json = json.loads( role_info_2 )
					#	print role_2_json[u'role']
					#except Exception:
					#	print "error parsing the json of the second id";
					#	break
	
					# we have both rid, now all we have to do is sen to the server to decide.
					json_obj = json.loads( authorization_double( "rfid_double", rid_1, rid_2, device_id ))
					print "\n"
					print json_obj
					print "\n"
					try:
						if json_obj[u'authorized'] == "Y":
							GPIO.output( pin_connect, True )
							GPIO.output( pin_led_ring, True )
							trans_id = json_obj[u'trans_id']
							time.sleep(0.5)
							GPIO.wait_for_edge( pin_button, GPIO.FALLING )
							end_trans( trans_id )
							GPIO.output( pin_connect, False )
							GPIO.output( pin_led_ring, False )
							break
						else:
							heart_beat()
							break
					except Exception:
						print "error parsing json of the authorization ... check to make sure the server is returning json."
						break
