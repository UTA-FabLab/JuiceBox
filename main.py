#!/usr/bin/python3

from __future__ import print_function
from juicebox import *
from gpio_connect import *
from safe_exit import *
import MFRC522

# Debug logging
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

# this is from the MFC library, it is to ensure safe exit
continue_reading = True

#main function
def main():
    GPIO.add_event_detect(pin_button, GPIO.FALLING) #to check whether button is pressed on the juicebox
    juicebox = Juicebox()   #creating the object to use the functions of class Juicebox()
    gpioconnect = ConnectgpioPins() #creating the object to use the functions of ConnectgpioPins()
    while continue_reading:         #reading the MFC library
        juicebox.go = False
        if (GPIO.event_detected(pin_button)):
#checking for the operator info
                (status, TagType) = MIFAREReader.MFRC522_Request(
                MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:    
                    gpioconnect.heart_beat()    #led blinks multiple times
                    juicebox.temp_rid = str(
                            uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    print("Operator RFID:", juicebox.temp_rid, file=sys.stdout)     #prints the operator RFID number after scanning
                    rid_1 = juicebox.temp_rid                                       #RFID number of operator is stored in variable rid_1
                    role_info = juicebox.check_status_operator(                     #getting the operator information
                    "check_status_rfid", juicebox.temp_rid)                         #and storing it in variable role_info
                    try:
                        role_json = json.loads(json.dumps(role_info))               #loads the json file and storing in variable role_json
                        print("Operator Level:",                                    #prints the operator level 
                            role_json["role"], file=sys.stderr)
                    except Exception:
                        print("JSON: ID_1 parse failure", file=sys.stderr)          #throwing exception if there is failure in getting correct json file
                        
                    juicebox.go = True                                              #changing the default value of attribute go and assigning it true
        #operator info is correct now checking for the staff info
                while juicebox.go == True:
                    (status, TagType) = MIFAREReader.MFRC522_Request(
                        MIFAREReader.PICC_REQIDL)
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        gpioconnect.heart_beat()
                        juicebox.temp_rid = str(uid[0]) + str(uid[1]) + \
                            str(uid[2]) + str(uid[3])
                        print("Staff RFID:", juicebox.temp_rid, file=sys.stderr)     #prints the operator RFID number after scanning
                        rid_2 = juicebox.temp_rid                                    #RFID number of staff is stored in variable rid_2
                        role_info_2 = juicebox.check_status_staff(                   #getting the staff information
                            "check_status_rfid", rid_2)                              #and storing it in variable role_info_2
                        try:
                            role_json_2 = json.loads(json.dumps(role_info_2))        #loads the json file and storing in variable role_json_2
                            print("Staff Level:",                                    #prints the operator level
                                role_json_2["role"], file=sys.stderr) 

                        except Exception:
                            print("JSON: ID_2 parse failure", file=sys.stderr)        #throwing exception if there is failure in getting correct json file
                            
                        json_obj = juicebox.authorization_double(                     #checking the information entered is correct for operator and staff
                            "rfid_double", rid_1, rid_2, device_id)                   #prints the status from information obtained from the json file
                        print("Status:", json_obj, file=sys.stderr)
                        try:                                                            
                            if json_obj['authorized'] == "Y":                         #checks if the user and staff is authorized
                                trans_id = json_obj['trans_id']                       #gets the transaction id from json object
                                time.sleep(0.5)
                                
                                end_obj = gpioconnect.end_trans()                     #ending the transaction and storing the value in variable end_obj
                                print("End Transaction:",end_obj,file=sys.stderr)                             #prints the End Transaction details
                                gpioconnect.refresh()                                 #changing the go attribute to False 
                                break
                            else:
                                gpioconnect.heart_beat()
                                gpioconnect.refresh()
                                break
                        except Exception:                                             #throwing the exception if the authorization or transaction fails
                            print(
                                "Error parsing json of the authorization ... check to make sure the server is returning json.", file=sys.stderr)
                            gpioconnect.refresh()
                            break
        
                        

        time.sleep(0.1)


if __name__ == '__main__':
    main()
    