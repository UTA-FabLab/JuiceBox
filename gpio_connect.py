from __future__ import print_function
import RPi.GPIO as GPIO
from juicebox import *
#GPIO pins
pin_button = 40
pin_green = 7
pin_red = 8
pin_connect = 3
pin_led_ring = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_connect, GPIO.OUT)
GPIO.output(pin_connect, False)
GPIO.setup(pin_led_ring, GPIO.OUT)
GPIO.output(pin_led_ring, False)
#subclass of Juicebox which contain the GPIO pins functions
class ConnectgpioPins(Juicebox): 
    #function for ending the transaction after user hits the juicebox button
    def end_trans(self):
        GPIO.output(pin_connect, True)          
        GPIO.output(pin_led_ring, True)
        time.sleep(0.5)
        GPIO.wait_for_edge(pin_button, GPIO.FALLING)
        payload = {"type": "end_transaction", "device": device_id}      
        
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