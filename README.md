# Design-Labolatory-MM_MS
  Xiaomi termometer <br>
  The goal of this project is to reprogram the TH05_v1.2 chip. This will allow the user to access the device settings and data received via Bluetooth.<br>
# Connecting
  The TH05 chip should be connected to the USB-UART converter as follows:
  
  Adapter      Device<br>
  GND     ->   -Vbat<br>
  +3.3V   ->   +Vbat<br>
  TX      ->    RX1<br>
  RX      ->    TX1<br>
  RTS     ->    RESET<br>

After wiring, install python 3 and the necessary libraries.<br>
```
pip3 install -r <requirements>   <br>
```
using the program “rdwr_phy62x2.py” run the file “BOOT_TH05F_v19.hex”  <br>
```
python3 rdwr_phy62x2.py -p COM<number> -e -r wh BOOT_TH05F_v19.hex 
```	
other options: <br>
```
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
```
Boot flashing is complete. The device is operational and the adapter can be disconnected.<br>

All of files and programs used to program the device and also all of the binaries where written by [pvvx](https://github.com/pvvx) and you can find it (as well as files to 
other chinese BTHome devices) on [his repo](https://github.com/pvvx/THB2). <br>
# Retrieving and Sending Data via Bluetooth
It is posible to comunicate with the device via Bluetooth. To do this we could either go to the [PHY62x2BTHome.html](https://pvvx.github.io/THB2/web/PHY62x2BTHome.html) website, written by 
the previous mentioned author or we could use a python code from this repo. <br>
It uses **bleak** and **asyncio** library to communicate with BLE device. We retrieve data from temperature and humidity sensor build-in TH05 thermometer, as well as battery percentage.
