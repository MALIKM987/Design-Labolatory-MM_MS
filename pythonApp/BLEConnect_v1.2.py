import asyncio
import array
from datetime import datetime
from time import sleep
from keyboard import is_pressed
from bleak import BleakScanner, BleakClient

#UUID needed for sending and receiving data
UUID_DEVICE = '0000fff4-0000-1000-8000-00805f9b34fb'
UUID_BATTERY = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_TEMP = '00002a6e-0000-1000-8000-00805f9b34fb'
UUID_HUMIDITY = '00002a6f-0000-1000-8000-00805f9b34fb'

######################################################################

#function for getting the data
async def get_device_info(client):
    now = datetime.now() #current time
    try:
        timeOfMeasure = now.strftime("%H:%M:%S")
        battery_level = await client.read_gatt_char(UUID_BATTERY)   #current battery lvl
        temp = await client.read_gatt_char(UUID_TEMP)               #current temperature
        humidity = await client.read_gatt_char(UUID_HUMIDITY)       #current humidity

        battery_level = int.from_bytes(battery_level, byteorder='little')
        temp = (int.from_bytes(temp, byteorder='little')) / 100
        humidity = (int.from_bytes(humidity, byteorder='little')) / 100
        #data conversion from binaries to readable data 

        print('{}: Battery: {}%; Temperature: {}°C; Humidity: {}% \n'.format(timeOfMeasure,battery_level,temp,humidity))
    except Exception as e:
        print(f"Error reading device info: {e}")

###########################################################

smiley=5 #on,1=off

###########################################3

#function used to connect to the device
async def connect(client):
    while(True):
        await client.disconnect()
        try:
            print("Connecting to the device...")
            await client.connect()
            print("Connected.")
            break
        except:
            print("Cannot connect. Reconnecting..")
            await client.disconnect()
            await asyncio.sleep(7)  #waits 7 seconds to fully disconect
            continue
        
async def main():
    interval = 0    #current interval
    #device search
    print("Searching for devices...")
    devices = await BleakScanner.discover(15.0)

    device_name = 'TH05F-582134'
    target_device = None

    for device in devices:
        if device.name == device_name:
            target_device = device
            break

    if not target_device:
        print(f"Device '{device_name}' not found.")
        return

    print(f"Found device: {target_device.address}")
    client = BleakClient(target_device.address)

    #Interval selection and retrieving data
    try:
        inChoice = True
        choice = 'i'
        while(inChoice):
            if(choice == 'q'):  #program quitting and disconnecting
                print("Disconnecting")
                await client.disconnect()
                print("Disconnect")
                break
            await connect(client)
            if(choice == 'i'):  #interval selection
                interval = input("Give me an interval in seconds: ")
                print("Setting an interval to " + interval + " seconds.")
                interval = float(interval)
                to_send = array.array('B', [85, smiley, 0, 0, 0, 63, 
                                    interval * 8, 29, 0, 2, 60, 180, 0]) #array to send

                await client.write_gatt_char(UUID_DEVICE, to_send)
                print("Reconection is needed.")
                await client.disconnect()
                print("Disconected")        #performing reconection to set up a new interval
                choice = 'r'
                continue
            elif(choice == 'r'): #retrieving data
                print("To quit program press and hold 'q' button.")
                print("To come back to selection of an interval press and hold 'r' button")
                while True:
                    await get_device_info(client)
                    sleep(interval)             #data
                    if(is_pressed('q')):        #quitting the program
                        print("Quitting...")
                        choice = 'q'
                        break
                    if(is_pressed('r')):        #going back to change the interval
                        print("Comming back...")
                        choice = 'i'
                        break
    except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":      #main initialization
    asyncio.run(main())
