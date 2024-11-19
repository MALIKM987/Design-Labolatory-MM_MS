import asyncio
import array
from datetime import datetime
from time import sleep
from keyboard import is_pressed
from bleak import BleakScanner, BleakClient

UUID_DEVICE = '0000fff4-0000-1000-8000-00805f9b34fb'
UUID_BATTERY = '00002a19-0000-1000-8000-00805f9b34fb'
UUID_TEMP = '00002a6e-0000-1000-8000-00805f9b34fb'
UUID_HUMIDITY = '00002a6f-0000-1000-8000-00805f9b34fb'

######################################################################

async def get_device_info(client):
    now = datetime.now()
    try:
        timeOfMeasure = now.strftime("%H:%M:%S")
        battery_level = await client.read_gatt_char(UUID_BATTERY)
        temp = await client.read_gatt_char(UUID_TEMP)
        humidity = await client.read_gatt_char(UUID_HUMIDITY)

        battery_level = int.from_bytes(battery_level, byteorder='little')
        temp = (int.from_bytes(temp, byteorder='little')) / 100
        humidity = (int.from_bytes(humidity, byteorder='little')) / 100

        print('{}: Battery: {}%; Temperature: {}°C; Humidity: {}% \n'.format(timeOfMeasure,battery_level,temp,humidity))
    except Exception as e:
        print(f"Error reading device info: {e}")

###########################################################

async def perform_ota(client, firmware_data):
    print("Starting OTA update...")
    try:
        for i in range(0, len(firmware_data), 20):  # BLE MTU is typically 20 bytes
            chunk = firmware_data[i:i + 20]
            await client.write_gatt_char(UUID_DEVICE, chunk)
            sleep(0.1)  # Add delay to avoid overloading the device
        print("OTA update completed.")
    except Exception as e:
        print(f"OTA update failed: {e}")

###########################################################

smiley=5 #on,1=off

###########################################3

async def connect(client):
    while(True):
        await client.disconnect()
        try:
            print("Connecting to device...")
            await client.connect()
            print("Connected.")
            break
        except:
            print("Cannot connect. Reconnecting..")
            await client.disconnect()
            await asyncio.sleep(7)
            continue
        
async def main():
    interval = 0
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

    try:
        inChoice = True
        choice = 'i'
        while(inChoice):
            if(choice == 'q'):
                await client.disconnect()
                print("Disconnect")
                break
            await connect(client)
            if(choice == 'i'):
                interval = input("Give me an interval in seconds: ")
                print("Setting an interval to " + interval + " seconds.")
                interval = int(interval)
                to_send = array.array('B', [85, smiley, 0, 0, 0, 63, interval * 8, 29, 0, 2, 60, 180, 0])
                await client.write_gatt_char(UUID_DEVICE, to_send)
                print("Reconection is needed.")
                await client.disconnect()
                print("Disconected")
                choice = 'r'
                continue
            elif(choice == 'r'):
                print("To quit program press and hold 'q' button.")
                print("To come back to selection of an interval press and hold 'r' button")
                while True:
                    await get_device_info(client)
                    sleep(interval)
                    if(is_pressed('q')):
                        choice = 'q'
                        break
                    if(is_pressed('r')):
                        choice = 'i'
                        break
    except Exception as e:
            print(f"An error occurred: {e}")




if __name__ == "__main__":
    asyncio.run(main())
