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
