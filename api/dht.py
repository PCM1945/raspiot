import Adafruit_DHT
import asyncio
from pydantic import BaseModel

sensor = Adafruit_DHT.DHT22
gpio_pin = 23 

def read_dht22():
    humidity, temp= Adafruit_DHT.read_retry(sensor, gpio_pin, 5)
    if humidity is not None and temp is not None:
        #print(f'Temperatura: {temp:.2f}°C')
        #print(f'Umidade: {humidity:.2f}%')
        return temp, humidity
    else:
        return None, None




# async def main():
#     while True:
#         try:
#             await read_dht22()
#         except KeyboardInterrupt:
#             break

# asyncio.run(main())

   