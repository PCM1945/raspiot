import aio_pika
import asyncio
import os
from dotenv import load_dotenv
import temp
import subprocess

# Load environment variables from the .env file
load_dotenv()

# Function to read the IP address of the RabbitMQ server from the .env file
def read_ip_from_env():
    ip = os.getenv('HOST_IP')
    return ip

# Function to send data to the RabbitMQ topic asynchronously
async def send_temperature_data(ip_address, message):
    try:
        # Connect to RabbitMQ server at the provided IP address
        connection = await aio_pika.connect_robust(f"amqp://{ip_address}/")
        async with connection:
            # Create a channel
            channel = await connection.channel()

            # Declare the 'temperature' exchange (topic)
            await channel.declare_exchange('temperature', aio_pika.ExchangeType.FANOUT)

            # Send the message to the 'temperature' exchange
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=''
            )

            print(f"Message '{message}' sent to the 'temperature' topic on server {ip_address}.")
    except Exception as e:
        print(f"Error while connecting or sending data to RabbitMQ: {e}")

# Function to wait until the IP address is available in the .env file
async def wait_for_ip():
    print(f"Waiting for the IP address in the .env file...")
    while True:
        ip = read_ip_from_env()
        if ip:
            print(f"IP address '{ip}' found. Proceeding with the connection...")
            return ip
        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

# olá mundo

# Main function to execute the script
async def main():
    
    try:
        open_hardware_monitor_path = os.getenv('OPEN_HARDWARE_MONITOR_PATH')
        if not open_hardware_monitor_path:
            print("The path to the OpenHardwareMonitor executable is not provided in the .env file.")
            abs_path = os.path.abspath(open_hardware_monitor_path)
            # Start the PowerShell script to run the OpenHardwareMonitor as an administrator
            subprocess.Popen(["powershell", "Start-Process",abs_path , "-Verb", "RunAs"], shell=True)
        while True:
            # Wait for the IP address to be available in the .env file
            ip_server = await wait_for_ip()

            # Data to be sent (temperature)
            temperature_message = temp.get_cpu_temperature() 

            # Send data to the RabbitMQ server asynchronously
            await send_temperature_data(ip_server, temperature_message)
    except KeyboardInterrupt:
        print("Script stopped.")
    

# Run the asyncio event loop
if __name__ == "__main__":

    asyncio.run(main())