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

Then connect the <b>Button</b> to the Raspberry pi. It is connected on <b>pin 40</b><br>
Then connect the <b>LED</b> to <b>pin 10</b> <br>
Then connect the Relay to pin 3 <br>

This is the full build of the power-tail. From here it is just software in order to complete it.<br><br>
### Software:
Assuming that you are starting from an older version of Rasbian( 2013 or older ), then you first need to enable SPI. To do that, type <b>sudo raspi-config</b> in order to enter the raspbian setup. Then go to advanced and enable SPI. Also you can change the hostname from this screen. If you have multiple JuiceBox, it is important that all JuiceBoxes have their own unique hostname.

1. You also have to install the SPI-Py library, since the RFID library uses it.vClone the library to your home directory and install it using the following commands:
		
		cd ~/
		git clone https://github.com/lthiery/SPI-Py
		cd ~/SPI-Py
		sudo python setup.py install
		
2. Moving back to the home directory, clone the JuiceBox repo:

		cd ~/
		git clone https://github.com/UTA-FabLab/JuiceBox
		
3. Move "on_boot" and "config.json" from the JuiceBox folder to the home directory:

		mv ~/Juicebox/on_boot ~/
		mv ~/Juicebox/config.json ~/
	
4. Start the JuiceBox instance using: 

		cd ~/JuiceBox
		sudo python final.py
		
##Additional notes:

To automatically start the JuiceBox instance at boot, use the "on_boot" script from the home directory. 

		cd ~/
		echo "sudo ./on_boot" >> ~/.bashrc
		
In addition to starting a JuiceBox instance, the "on_boot" does the following: 

1. It will run the check_net.py script, allowing the device to display a flashing LED until it is connected to the network.
2. It will also launch the watchdog script, allowing the process to restart if it fails.

Notes:
  - The URL and Device ID are in ~/config.json
  - If you plan on using the keyswipe powertail, you must clone a different branch add -b magnetic_sw to the git clone command
  - for magnetic stripe, you MUST use bashrc to boot the script
  - You can use cron to automate the JuiceBox instead of the .bashrc.



