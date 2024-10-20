from phue import Bridge
from config import HUE_BRIDGE
# Connect to the Hue Bridge
  # Replace with your Bridge's IP
b = Bridge(HUE_BRIDGE)
b.connect()  # Connect to the bridge

# List all lights and their IDs
lights = b.lights
for light in lights:
    print(f"Light Name: {light.name}, Light ID: {light.light_id}")
