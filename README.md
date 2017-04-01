# JuiceBox

### Goals:
1. We want a device that can scan RFID tags, send the data to our server and decide whether to turn the machines on/off
2. The device will have an RFID reader, MFRC522 to be exact.
3. It controls the machines via a powertail ( Relay )

### Intended Use:
1. First we place the RFID tag infront of the scanner.
2. we press the button, the device will now take in a scan and a light will indicate this.
    * If the scan was succesful ( the server gave an appropriate response ), we can move on to the next step. The LED will indicate this.
    * If NOT -- The LED will indicate an error and the process restarts.
3. the device is now waiting for another RFID card to scan. ( It needs two RFIDs 1 for the user and 1 for the employee )
4. If the scans are good and the server return an OK, the LED will come on and the relay will trigger the tool
5. If the scans are bad and server return a NO, the LED will indicate and error and the process will restart

## Building a JuiceBox:

First you must connect all the components to the PI. The first would be the RFID Reader. The connections are available on the Github for the library needed to use it. I have pasted the connections below:
	
|Name | Pin #  | Pin name     |
| --- | ------ | ------       |
|SDA  |  24    |	GPIO8       |
|SCK  |	23    |	GPIO11      |
|MOSI	|  19	   |  GPIO10      |
|MISO	|  21    |	GPIO9       |
|IRQ	|  None	|  None        |
|GND	|  Any   |	Any Ground  |
|RST	|  22    |	GPIO25      |
|3.3V	|  1     |	3V3         |

Then connect the Button to the Raspberry pi. It is connected on pin 40<br>
Then connect the LED to pin 10 <br>
Then connect the Relay to pin 3 <br>
