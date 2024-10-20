from phue import Bridge

class HueController:
    def __init__(self, bridge_ip):
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()  # Connect to the bridge

    def turn_on(self, light_id):
        self.bridge.set_light(light_id, 'on', True)

    def turn_off(self, light_id):
        self.bridge.set_light(light_id, 'on', False)

    def set_brightness(self, light_id, brightness):
        # Brightness should be between 0 (off) and 254 (full brightness)
        self.bridge.set_light(light_id, 'bri', brightness)
        
    def get_brightness(self, light_id):
        # This is a placeholder; implement your logic to get brightness
        light_state = self.bridge.get_light(light_id)  # Replace with your actual method to get light state
        return light_state.get('bri', 0)