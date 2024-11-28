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
  '-p' = Serial port device
  '-b' = Set Port Baud (115200, 250000, 500000, 1000000)
  '-a' = Pre-processing: All Chip Erase
  '-e' = Pre-processing: Erase Flash work area
  '-r' = Post-processing: Reset
  '-s' = Application start address for hex writer
  '-w' = Flash starting address for hex writer
  'wh' = Write hex file to Flash
  'we' = Write bin file to Flash with sectors erases
  'filename'  = Name of binary file
  'wf' = Write bin file to Flash without sectors erases
  'er' = Erase Region (sectors) of Flash
  'ew' = Erase Flash Work Area
  'ea' = Erase All Flash (MAC, ChipID/IV)
  'rc' = Read chip bus address to binary file
```
Boot flashing is complete. The device is operational and the adapter can be disconnected.<br>

All of files and programs used to program the device and also all of the binaries where written by [pvvx](https://github.com/pvvx) and you can find it (as well as files to 
other chinese BTHome devices) on [his repo](https://github.com/pvvx/THB2). <br>
Now you have to flash a proper firmware into device. To do this you should:
1. Open the website - [PHY62x2BTHome.html](https://pvvx.github.io/THB2/web/PHY62x2BTHome.html),
2. Connect to the device via it,
3. Go to `OTA` tab, select the proper `.bin` file,
4. Click `Start`
After this, the firmware should be flashed.

Alternatively, you could do this via UART adapter. By connecting the device into it and running this command:
```
python3 rdwr_phy62x2.py -p COM11 -r we 0x10000 TH05_v19.bin
```
in your command prompt. Of course instead of `COM11` you should write the port curently used by the connected adapter. 
# Retrieving and Sending Data via Bluetooth
It is posible to comunicate with the device via Bluetooth. To do this we could either go to the [PHY62x2BTHome.html](https://pvvx.github.io/THB2/web/PHY62x2BTHome.html) website, written by 
the previous mentioned author or we could use a python code from this repo. <br>
It uses **bleak** and **asyncio** library to communicate with BLE device. We retrieve data from temperature and humidity sensor build-in TH05 thermometer, as well as battery percentage. <br>
To use the newest version of the program you have to clone this repository on your PC by typing: 
```
git clone https://github.com/MALIKM987/Design-Labolatory-MM_MS.git
```
in your command prompt. Then run **start.bat** file.<br>
Firstly the program will search the available device. If it founds it, it will try to connect, if not you could restart the program and try again. <br>
After searching, it will try to connect. The program is written that way, that it will try to connect until the end. Typically it takes 2 or 3 times till it is fully connected. <br>
Next you will be asked to type in an interval of receiving data. After this the thermometer will reconnect. For some reason the larger the interval, the more tries it takes to connect again. <br>
If the reconnection process goes well, you will see the data being received by your PC. <br>
To stop receiving data, you must press and hold 'q' button. The 'r' button allows you to change an interval.
