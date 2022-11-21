# Smart_streetlighting[README.txt](https://github.com/atanu22-iitk/Smart_streetlighting/files/10056196/README.txt)
Raspberry PI:-

Move to 'Pi Code' folder

The python files and their functionality is as follows -

Individual modules -
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. pi_pir.py - The code for PIR interfacing with Raspberry Pi.
2. pi_ldr.py - The code for LDR interfacing with Raspberry Pi.
3. pi_gps.py - The code for GPS interfacing with Raspberry Pi.
4. pi_transmitter.py - Code to configure as the transmitter and manually tranmit data packet from Pi to Pi.(Path - Pi Code\RPi_code\SX127x)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

NOTE: - The RPi_code folder contains all the python package files which will be required to run receiver-uno.py and pi_transmitter.py files.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

Combined Code for complete model functionality -
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. receiver-uno.py - Configures Raspberry Pi as a gateway node. Running the python file the Pi entires receiving mode waiting for information from the 
sensor nodes and work accordingly.

The checklist before running the receiver-uno.py and pi_transmitter.py files -

1. Login to Raspberry Pi using VNC viewer or ssh to the IP address of Pi and run the below commands -
	- sudo raspi-config (Opens configuration window of Pi)
	- Enable the SPI interface and exit the configuration window.
	- pip install RPi.GPIO
	- pip install spidev
	- pip install pyLoRa
	- sudo apt-get install python-rpi.gpio python3-rpi.gpio
	- sudo apt-get install python-spidev python3-spidev

2. Check that the following python files are in the folder SX127x -
	- LoRa.py
	- board_config.py
	- contants.py
	- __init__.py
	- LoRaArgumentParser.py
	
3. In case the receiver-uno.py and pi_transmitter.py files give error of file not found for the packages included check the path of the folder in the below line 
present in the python files-

sys.path.insert(0, '../../RPi_code') 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

Arduino UNO :- 

Install Arduino IDE and upload below mentioned files in arduino uno dev-board.

Inside the 'Arduino code' folder
There are three INO files for three arduino in the corresponding folders.

Arduino1 -> Arduino1.ino
Arduino2 -> Arduino2.ino
Arduino3 -> Arduino3.ino

All the libraries are there inside the 'libraries' folder

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

Hardware Configuration -

The hardware configuration of all the modules with Raspberry Pi and Arduino are present in the Hardware_config.doc file.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

