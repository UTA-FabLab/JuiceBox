# JuiceBox

### Goals:
1. A device to intake user credentials, authenticate against granted rights, and enable/disable usage based on those.
2. Utilize RFID as a medium for user credentials.
3. Control usage of the machines via controlling power to it. 

### Usage:
1. Place a user's RFID tag in front of the scanner.
2. Press the button to scan tag, light will indicate scan status - 
    <br>If the scan was succesful, the LED will blink once.
    <br>If NOT -- The LED will blink multiple times and the sequence will reset.
3. Place a staff member's RFID tag in front of the scanner and press the button
4. If permissions are correct, JuiceBox will blink the LED once and then leave it on.
5. If permissions are incorrect, JuiceBox will blink the LED multiple times and the sequence will reset

## Building a JuiceBox:

The MFRC22 reader we currently employ works via SPI interface, pinout scheme is listed below:

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

Connect the <b>Button switch</b> poles to <b>GPIO 40</b> and <b>Ground</b><br>

Connect the <b>LED</b> to <b>GPIO 10</b> and <b>Ground</b> <br>

Connect the Relay to <b>GPIO 3</b> and <b>Ground</b> <br>

<br><br>
### Software:
Assuming that you are starting from an older version of Rasbian( 2013 or older ):
<br><br>
1.	Enable SPI - type <b>sudo raspi-config</b> in order to enter the raspbian setup.  Go to Advanced and check Enable SPI. If desired, the hostname can be changed on this menu as well.  If you have multiple JuiceBox, it is crucia that all JuiceBoxes have their  unique hostnames.

2. Install the SPI-Py library.  vClone the library to your home directory and install it using the following commands:
		
		cd ~/
		git clone https://github.com/lthiery/SPI-Py
		cd ~/SPI-Py
		sudo python setup.py install
		
2. Move back to the home directory and clone the JuiceBox repo:

		cd ~/
		git clone https://github.com/UTA-FabLab/JuiceBox
		
3. Move "on_boot" and "config.json" from the JuiceBox folder to the home directory:

		mv ~/Juicebox/on_boot ~/
		mv ~/Juicebox/config.json ~/
	
4. Start a JuiceBox instance: 

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
  - If you plan on using a magswipe to authenticate users, you must clone a different branch:<br>	add -b magnetic_sw to the git clone command
  - For magswipe to work, you currently MUST use bashrc to boot the script
  - You can use cron to automate the JuiceBox instead of the .bashrc.



