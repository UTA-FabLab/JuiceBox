"""This program consist of the functions which are used in main.py file for operating the GPIO pins and ending the transaction when the operator presses the button on JuiceBox
    """
from __future__ import print_function
import RPi.GPIO as GPIO
from juicebox import *
# GPIO pins
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
# subclass of Juicebox which contain the GPIO pins functions


class ConnectgpioPins(Juicebox):
    """This class is the subclass of Juicebox which contain the GPIO pins utility and ending transaction functionality

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
    # function for ending the transaction after user hits the juicebox button

    def end_trans(self):
        """This function is used to end the transaction when the operator hits the JuiceBox button. It ends the ticket that was initiated on the FabApp Dashboard

        Returns:
            str: It prints the success message with ticket number that has been closed
        """
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
        except Exception as e:
            response = "could not end transaction"
            print(response, file=sys.stderr)
            raise e

        GPIO.output(pin_connect, False)
        GPIO.output(pin_led_ring, False)
        return response

    def heart_beat(self):
        """This function is used to show output on the JuiceBox device by blinking the LED ligths. After the operator scans their tokens it is validated and if the information is correct it blinks once and solid red light is displayed. If the information is not correct it blinks multiple times and shuts down.
        """
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
        """This function is used to refresh the JuiceBox for the next time use
        """
        self.go = False
# end of subclass
