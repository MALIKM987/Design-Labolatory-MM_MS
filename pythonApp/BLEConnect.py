import asyncio
import array
from time import sleep
from bleak import BleakScanner, BleakClient

uuidForDevice = '0000fff4-0000-1000-8000-00805f9b34fb' 
uuidForBattery = '00002a19-0000-1000-8000-00805f9b34fb' 
uuidForTemp = '00002a6e-0000-1000-8000-00805f9b34fb' 
uuidForHum = '00002a6f-0000-1000-8000-00805f9b34fb'
#38:1F:8D:58:21:34
def swap_Endians(value):
    first = (value & eval('0x00FF')) >> 0
    second = (value & eval('0xFF00')) >> 8
    first <<= 8
    second <<= 0
    result = (first | second ) 
    return result

async def main():
    toSend = array.array('B', [85, 5, 0, 0, 0, 63, 8, 29, 0, 2, 60, 180,0] )
    chances = 500
    termometr = ''
    print("Searching device...")
    devices = await BleakScanner.discover(15.0, return_adv=True)
    for d in devices:
        if(devices[d][1].local_name=='TH05F-582134'):
            print("Got it")
            termometr = d
    addres = termometr
    print(addres)
    client = BleakClient(addres)
    print("Connecting...")
    
    await client.connect()
    print("Conected :)")
    #85 1 0 0 0 63 8 29 0 2 60 180 0 -smiley off
    #85 5 0 0 0 63 8 29 0 2 60 180 0 -smiley on
    await client.write_gatt_char(uuidForDevice, toSend)
    while(chances != 0):
        try:
            temp = await client.read_gatt_char(uuidForTemp) 
            print(swap_Endians(int.from_bytes(temp))/100)
            sleep(1)
        except:
            print("An error ocured")
        chances = chances-1

    print("Cannot conect :(")
    await client.disconnect()

asyncio.run(main())