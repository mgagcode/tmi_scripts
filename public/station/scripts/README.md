# TMI Demo Example Scripts
## prod_v0
* Three examples
  * prod_0
    * shows all APIs in use
    * shows the extended record TMIBasicKeysV1
  * prod_1
    * shows how "subs" work in replacing values in a script
  * prod_2
    * shows how multiple tests work
* These examples use the "fake" HWDRV, which sets the number of channels
  * As an experiment, edit the driver (./public/station/drivers/fake/tmi_fake.py) and change NUM_CHANNELS up to 4
## dso_v0
* example connecting to an Agilent DSO7104B using the VISA modules
  * without the DSO, the system will fail to run the script
* As an experiment, if you have a similiar Agilent DSO, you should be able to modify the driver and use youre scope
  * see ./public/station/drivers/agilent_dso_usb_1  
## pybrd_v1
* MicroPython script example for use with the demo Micropython test fixture
  * without the MicroPython boards, the system will fail to find the hardware and will not run
* Demonstrates how 
  * HWDRV detects up to 4 USB connected MicroPython boards
  * PLAY driven from the hardware
  * ADC measurements
  * etc 
