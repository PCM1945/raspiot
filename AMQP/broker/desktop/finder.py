from zeroconf import ServiceBrowser, Zeroconf

class MyServiceListener:
    def add_service(self, zeroconf, service_type, name):
        print(f"Service added: {name}")
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print_service_info(info)

    def remove_service(self, zeroconf, service_type, name):
        print(f"Service removed: {name}")

    def update_service(self, zeroconf, service_type, name):
        print(f"Service updated: {name}")
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print_service_info(info)

def print_service_info(info):
    """Print details of the discovered service."""
    print("Service Info:")
    print(f"  Name: {info.name}")
    print(f"  Type: {info.type}")
    print(f"  Address: {info.parsed_addresses()}")
    print(f"  Port: {info.port}")
    print(f"  Properties: {info.properties}")

def main():
    zeroconf = Zeroconf()
    listener = MyServiceListener()

    try:
        print("Browsing for services...")
        # Replace '_example._tcp.local.' with the service type you want to discover
        browser = ServiceBrowser(zeroconf, "_example._tcp.local.", listener)

        print("Press Ctrl+C to stop.")
        input("Press Enter to exit...\n")
    finally:
        print("Stopping Zeroconf...")
        zeroconf.close()

if __name__ == "__main__":
    main()