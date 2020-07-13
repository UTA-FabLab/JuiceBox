#!/usr/bin/python2.7

from __future__ import print_function
from juicebox import *
from gpio_connect import *
from safe_exit import *
import MFRC522

# Debug logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig(format='%(asctime)s %(message)s')
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger('requests.packages.urllib3')
req_log.setLevel(logging.DEBUG)
req_log.propagate = True

# this is from the MFC library, it is to ensure safe exit
continue_reading = True
#main function

def main():
    GPIO.add_event_detect(pin_button, GPIO.FALLING)
    juicebox = Juicebox()
    gpioconnect = ConnectgpioPins()
    while continue_reading:
        juicebox.go = False
        if (GPIO.event_detected(pin_button)):

                (status, TagType) = MIFAREReader.MFRC522_Request(
                MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                if status == MIFAREReader.MI_OK:
                    gpioconnect.heart_beat()
                    juicebox.temp_rid = str(
                            uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    print("Operator RFID:", juicebox.temp_rid, file=sys.stderr)
                    rid_1 = juicebox.temp_rid
                    role_info = juicebox.check_status_operator(
                    "check_status_rfid", juicebox.temp_rid)
                    try:
                        role_json = json.loads(json.dumps(role_info))
                        print("Operator Level:",
                            role_json["role"], file=sys.stderr)
                    except Exception:
                        print("JSON: ID_1 parse failure", file=sys.stderr)
                        
                    juicebox.go = True
                    #operator info is correct then check for staff
                while juicebox.go == True:
                    (status, TagType) = MIFAREReader.MFRC522_Request(
                        MIFAREReader.PICC_REQIDL)
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        gpioconnect.heart_beat()
                        juicebox.temp_rid = str(uid[0]) + str(uid[1]) + \
                            str(uid[2]) + str(uid[3])
                        print("Staff RFID:", juicebox.temp_rid, file=sys.stderr)
                        rid_2 = juicebox.temp_rid
                        role_info_2 = juicebox.check_status_staff(
                            "check_status_rfid", rid_2)
                        try:
                            role_json_2 = json.loads(json.dumps(role_info_2))
                            print("Staff Level:",
                                role_json_2["role"], file=sys.stderr) 

                        except Exception:
                            print("JSON: ID_2 parse failure", file=sys.stderr)
                            
                        json_obj = juicebox.authorization_double(
                            "rfid_double", rid_1, rid_2, device_id)
                        print("Status:", json_obj, file=sys.stderr)
                        try:
                            if json_obj[u'authorized'] == "Y":
                                trans_id = json_obj[u'trans_id']
                                time.sleep(0.5)
                                
                                end_obj = gpioconnect.end_trans()
                                print("End Transaction:",
                                      end_obj, file=sys.stderr)
                                gpioconnect.refresh()
                                break
                            else:
                                gpioconnect.heart_beat()
                                gpioconnect.refresh()
                                break
                        except Exception:
                            print(
                                "Error parsing json of the authorization ... check to make sure the server is returning json.", file=sys.stderr)
                            gpioconnect.refresh()
                            break
        
                        

        time.sleep(0.1)


if __name__ == '__main__':
    main()
    