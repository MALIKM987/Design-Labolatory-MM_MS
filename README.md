# Design-Labolatory-MM_MS
  Xiaomi termometer 
  The goal of this project is to reprogram the TH05_v1.2 chip. This will allow the user to access the device settings and data received via Bluetooth.
# Connecting
  The TH05 chip should be connected to the USB-UART converter as follows:
  
  Adapter      Device<br>
  GND     ->   -Vbat<br>
  +3.3V   ->   +Vbat<br>
  TX      ->    RX1<br>
  RX      ->    TX1<br>
  RTS     ->    RESET<br>

After wiring, install python 3 and the necessary libraries.<br>
pip3 install -r <requirements>   <br>
<br>
<br>
using the program “rdwr_phy62x2.py” run the file “BOOT_TH05F_v19.hex”  <br>
    python3 rdwr_phy62x2.py -p COM<number> -e -r wh BOOT_TH05F_v19.hex
other option <br>
  '-p' = Serial port device<br>
  '-b' = Set Port Baud (115200, 250000, 500000, 1000000)<br>
  '-a' = Pre-processing: All Chip Erase<br>
	'-e' = Pre-processing: Erase Flash work area<br>
	'-r' = Post-processing: Reset<br>
	'-s' = Application start address for hex writer<br>
  '-w' = Flash starting address for hex writer<br>
	'wh' = Write hex file to Flash<br>
  'we' = Write bin file to Flash with sectors erases<br>
  'filename'  = Name of binary file<br>
  'wf' = Write bin file to Flash without sectors erases<br>
	'er' = Erase Region (sectors) of Flash<br>
  'ew' = 'Erase Flash Work Area')v
  'ea' = 'Erase All Flash (MAC, ChipID/IV)')<br>
  'rc' = 'Read chip bus address to binary file')<br>
<br>
Boot flashing is complete. The device is operational and the adapter can be disconnected.<br>
