from zeroconf import ServiceInfo, Zeroconf, ZeroconfServiceTypes
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor

class AsyncZeroconf:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.executor = ThreadPoolExecutor()

    async def register_service(self, info):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.register_service, info)

    async def unregister_service(self, info):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.unregister_service, info)

    async def close(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.executor, self.zeroconf.close)

async def main():
    # Define service details
    service_type = "_smartHome._tcp.local."
    service_name = "SmartHome._example._tcp.local."
    port = 12345  # Port the service runs on
    # Obtém o nome do host
    hostname = socket.gethostname()
    # Obtém o endereço IP associado ao nome do host
    ip_address = socket.gethostbyname(hostname)
    address = socket.inet_aton(ip_address)  # Replace with your IP
    properties = {"version": "1.0"}  # Service metadata

    # Create service info
    info = ServiceInfo(
        service_type,
        service_name,
        addresses=[address],
        port=port,
        properties=properties,
        server=f"{hostname}.local."
    )

    # Set up asynchronous Zeroconf
    async_zeroconf = AsyncZeroconf()

    try:
        print("Registering service...")
        await async_zeroconf.register_service(info)
        print(f"Service '{service_name}' registered. Running async server...")
        
        # Keep the service running
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Shutting down service...")
    finally:
        print("Unregistering service...")
        await async_zeroconf.unregister_service(info)
        await async_zeroconf.close()
        print("Service unregistered and zeroconf closed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user.")