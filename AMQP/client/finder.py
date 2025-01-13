from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
import asyncio
import dotenv
import logging
import os 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filemode= 'w', filename='finder.log')
dotenv.load_dotenv()

class MyServiceListener:

    def write_ip():
        with open(".env", "r") as f:
            for line in f.readlines():
                try:
                    key, value = line.split('=')
                    os.putenv(key, value)
                except ValueError:
                    # syntax error
                    pass

    def on_service_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        logging.info(f"Service added: {name}")
        print(f"Service added: {name}")

        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            print(f"Service added: {name}")
        if state_change is ServiceStateChange.Removed:
            print(f"Service removed: {name}")
            info = zeroconf.get_service_info(service_type, name)
        if state_change is ServiceStateChange.Updated:
            print(f"Service updated: {name}")
            info = zeroconf.get_service_info(service_type, name)
        if info:
            self.print_service_info(info)

    def print_service_info(self, info):
        """Print details of the discovered service."""
        info_string = f"""
            Service Info: \n
            Name: {info.name}\n
            Type: {info.type}\n
            Address: {info.parsed_addresses()}\n
            Port: {info.port}\n
            Properties: {info.properties}\n
        """
        print(info_string)
        logging.info(info_string)

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
        logging.info(f"Browsing for services of type '{self.service_type}'...")
        print(f"Browsing for services of type '{self.service_type}'...")
        ServiceBrowser(self.zeroconf, self.service_type, handlers=[self.listener.on_service_change], )

    async def stop_browser(self):
        """Stop browsing for services."""
        logging.info("Stopping service browser...")
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

    except asyncio.CancelledError:
        print("\nStopping...")
    finally:
        await browser.stop_browser()

if __name__ == "__main__":
    asyncio.run(main())
