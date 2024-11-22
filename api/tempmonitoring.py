import Adafruit_DHT
import asyncio
import csv
import datetime



# using now() to get current time


sensor = Adafruit_DHT.DHT22
gpio_pin = 23 

async def read_dht22():
    humidity, temp= Adafruit_DHT.read_retry(sensor, gpio_pin, 5)

    if humidity is not None and temp is not None:
        current_time = datetime.datetime.now() 
        print(f'time: {current_time}')
        print(f'Temperatura: {temp:.2f}°C')
        print(f'Umidade: {humidity:.2f}%')
        await asyncio.sleep(2)
    else:
        print('Fail reading')



async def main():
    while True:
        try:
            await read_dht22()
        except KeyboardInterrupt:
            break

asyncio.run(main())

   