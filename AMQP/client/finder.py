from zeroconf import ServiceBrowser, Zeroconf
import asyncio

class MyServiceListener:
    def add_service(self, zeroconf, service_type, name):
        print(f"Service added: {name}")
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.print_service_info(info)

    def remove_service(self, zeroconf, service_type, name):
        print(f"Service removed: {name}")

    def update_service(self, zeroconf, service_type, name):
        print(f"Service updated: {name}")
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.print_service_info(info)

    def print_service_info(self, info):
        """Print details of the discovered service."""
        print("Service Info:")
        print(f"  Name: {info.name}")
        print(f"  Type: {info.type}")
        print(f"  Address: {info.parsed_addresses()}")
        print(f"  Port: {info.port}")
        print(f"  Properties: {info.properties}")

class AsyncZeroconfBrowser:
    def __init__(self, service_type):
        self.zeroconf = Zeroconf()
        self.service_type = service_type
        self.listener = MyServiceListener()

    async def start_browser(self):
        """Start browsing for services asynchronously."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._start_browser)

    def _start_browser(self):
        """Run the service browser in a separate thread."""
        print(f"Browsing for services of type '{self.service_type}'...")
        ServiceBrowser(self.zeroconf, self.service_type, self.listener)

    async def stop_browser(self):
        """Stop browsing for services."""
        print("Stopping service browser...")
        self.zeroconf.close()

async def main():
    service_type = "_example._tcp.local."  # Change this to the service type you're looking for
    browser = AsyncZeroconfBrowser(service_type)

    try:
        await browser.start_browser()
        print("Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await browser.stop_browser()

if __name__ == "__main__":
    asyncio.run(main())
