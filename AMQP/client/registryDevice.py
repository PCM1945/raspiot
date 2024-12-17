from zeroconf import ServiceInfo, Zeroconf
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
import getip

class AsyncZeroconfClient:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.executor = ThreadPoolExecutor()

    async def register_service(self, info):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.register_service, info)
        print(f"Service '{info.name}' registered.")

    async def unregister_service(self, info):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.unregister_service, info)
        print(f"Service '{info.name}' unregistered.")

    async def close(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.close)
        print("Zeroconf closed.")

async def client_register():
    # Define client service details
    service_type = "_smartHome._tcp.local."  # Service type
    service_name = "smartHome._smartHome._tcp.local."  # Client's service name
    port = 23456  # Port where the client may listen for requests
    ip_address = getip.get_local_ip() # Local IP address
    properties = {"role": "client", "version": "1.0"}  # Optional metadata

    # Convert IP to bytes
    address = socket.inet_aton(ip_address)

    # Create ServiceInfo for the client
    info = ServiceInfo(
        service_type,
        service_name,
        addresses=[address],
        port=port,
        properties=properties,
        server=f"{socket.gethostname()}.local."  # Hostname
    )

    async_zeroconf = AsyncZeroconfClient()

    try:
        print(f"Registering client '{service_name}'...")
        await async_zeroconf.register_service(info)

        # Keep the service alive indefinitely
        print("Client is running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        print("\nClient shutting down...")
    finally:
        await async_zeroconf.unregister_service(info)
        await async_zeroconf.close()

if __name__ == "__main__":
    try:
        asyncio.run(client_register())
    except KeyboardInterrupt:
        print("\nClient stopped by user.")