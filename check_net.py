import requests
import time
import RPi.GPIO as GPIO

url = "http://google.com"
pin_led = 33
led_on = False
blink_time = 1

GPIO.setmode( GPIO.BOARD )
GPIO.setup( pin_led, GPIO.OUT )


# infinit while loop to check for internet conncetion 
while True:
	# try to connect using requests library ..... if succesful, BREAK
	try:
		requests.get( url )
		break
	# otherwise print no conn and blink the led ring
	except Exception:
		if led_on == False:
			GPIO.output( pin_led, False )
		else:
			GPIO.output( pin_led, True )			
	
	time.sleep( blink_time )
	if led_on == True:
		led_on = False
	else:
		led_on = True

GPIO.output( pin_led, False )
