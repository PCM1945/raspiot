import asyncio
import wmi

async def get_cpu_temperature():
    """Fetch CPU temperature using WMI."""
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                return sensor.Value
    except Exception as e:
        print(f"Error fetching CPU temperature: {e}")
    return None

async def monitoring():
    """Monitor CPU temperature asynchronously."""
    while True:
        temp = await get_cpu_temperature()
        if temp is not None:
            print(f"CPU Temperature: {temp:.2f}°C")
        else:
            print("Unable to fetch CPU temperature.")
        await asyncio.sleep(2)  # Wait for 2 seconds before next check

async def main():
    """Main function to start monitoring."""
    try:
        await monitoring()
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    asyncio.run(main())