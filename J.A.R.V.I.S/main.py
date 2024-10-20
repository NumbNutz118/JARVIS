from speech_handler import recognize_speech
from text_to_speech import speak
from openai_handler import get_openai_response, get_chatgpt_response
from weather_handler import get_weather
import time
from light_control import HueController
from config import HUE_BRIDGE, LIGHT_ID
import music_player
import threading

hue = HueController(HUE_BRIDGE)

def handle_weather_query(user_input):
    weather_info = get_weather(query="full")
    time.sleep(2)
    return weather_info, get_openai_response(f"The current weather is: {weather_info}. {user_input}")

def handle_weather_query_tomorrow(user_input):
    weather_info = get_weather(query="next day")
    return weather_info, get_openai_response(f"Tomorrow's weather is: {weather_info}. {user_input}")

def music_playing():
    if music_player.is_music_playing:
        return True

# Initialize memory
memory = {
    "light": None,
    "weather": {
        "current": None,
        "tomorrow": None
    },
    "activity": None,
    "music": None,
    "last_response": None
}

def process_command(user_input):
    global memory, current_music_thread  # Make sure to access the global memory variable
    # Define the main categories for processing
    
    if music_player.is_music_playing and "jarvis" in user_input:
        music_player.pause_music()
        speak("Music paused. What can I do for you?")
        return  # Stop further processing to await next command
    
    categories = {
        "bright lighting": ["turn on", "increase", "brighter", "more light"],
        "dark lighting": ["turn off", "decrease", "dimmer", "less light"],
        "weather": ["current weather", "tomorrow's weather", "forecast"],
        "weather activity": ["good day for", "suitable activity", "plan for", "ideal conditions", "weather for"],
        "general": ["tell me", "say", "information", "help"],
        "music": ["play", "pause", "next", "previous", "resume", "stop"]
    }

    # Get the intent from ChatGPT, allowing for full-sentence inputs
    intent_response = get_chatgpt_response(
        f"Given the following user input: '{user_input}', and your current memory: {memory}, what action should be taken based on these categories: {', '.join(categories.keys())}?"
    )
    action = intent_response.strip().lower()  # Extract the action from the response

    print(f"Action determined: {action}")

    # Handle different actions based on the response
    if "weather" in action:
        if "tomorrow" in user_input or "that" in user_input:
            last_weather_info, info = handle_weather_query_tomorrow(user_input)
            memory["weather"]["tomorrow"] = info  # Store weather info in memory
            response = get_openai_response(f"Given the forecast weather info: {info}. {user_input}")
            speak(response)
            memory["last_response"] = response
            if memory.get("music", True):
                music_player.resume_music()
            
        else:
            last_weather_info, info = handle_weather_query(user_input)
            memory["weather"]["current"] = info  # Store current weather info in memory
            response = get_openai_response(f"Given the current weather info: {info}. {user_input}")
            speak(response)
            memory["last_response"] = response
            if memory.get("music", True):
                music_player.resume_music()
            

    elif "light" in action:
        if "turn on" in action or "turn the light on" in action or "light on" in action:
            hue.turn_on(LIGHT_ID)
            memory["light"] = "on"  # Update memory
            speak("The light is now on.")
            if memory.get("music", True):
                music_player.resume_music()
            
        elif "turn off" in action or "turn the light off" in action or "light off" in action:
            hue.turn_off(LIGHT_ID)
            memory["light"] = "off"  # Update memory
            speak("The light is now off.")
            if memory.get("music", True):
                music_player.resume_music()
            
        elif "increase" in action or "brighter" in action or "more bright" in action or "bright" in action:
            # Increase brightness logic here
            current_brightness = hue.get_brightness(LIGHT_ID)
            new_brightness = min(254, current_brightness + 50)  # Increase by 50
            hue.set_brightness(LIGHT_ID, new_brightness)
            brightness_percentage = round(new_brightness / 254 * 100)
            memory["light"] = new_brightness  # Store brightness level in memory
            speak(f"The light brightness is now adjusted to {brightness_percentage}%")
            if memory.get("music", True):
                music_player.resume_music()
            
        elif "decrease" in action or "dimmer" in action or "less bright" in action or "dark" in action or "darker" in action:
            # Decrease brightness logic here
            current_brightness = hue.get_brightness(LIGHT_ID)
            new_brightness = max(0, current_brightness - 50)  # Decrease by 50
            hue.set_brightness(LIGHT_ID, new_brightness)
            brightness_percentage = round(new_brightness / 254 * 100)
            memory["light"] = new_brightness  # Store brightness level in memory
            speak(f"The light brightness is now adjusted to {brightness_percentage}%")
            if memory.get("music", True):
                music_player.resume_music()
            
    
    elif "good day for" in action:
        activity = user_input.split("good day for")[-1].strip()  # Extract activity from input
        if memory["weather"]:  # Check if there's weather memory
            prompt = f"Based on the following weather information: '{memory['weather']}', is it a good day for {activity}?"
            response = get_openai_response(prompt)
            speak(response)
            memory["last_response"] = response
            if memory.get("music", True):
                music_player.resume_music()
            
        else:
            prompt = f"Based on the current weather, is it a good day for {activity}?"
            response = get_openai_response(prompt)
            speak(response)
            memory["last_response"] = response
            if memory.get("music", True):
                music_player.resume_music()
            
            
    elif "music" in action:
        if "play" in action:
            query = user_input.lower()
            if query.startswith('play '):
                speak(query.lower().replace("play", "Now playing"))
                query = query[5:].strip()
                current_music_thread = threading.Thread(target=start_music_player, args=(query,))
                current_music_thread.start()
                memory["music"] = True
        elif "pause" in action:
            music_player.pause_music()
        elif "resume" in action:
            music_player.resume_music()
        elif "stop" in action:
            music_player.stop_music()
            speak("Music has been stopped.")
            memory["music"] = False
            
        recognize_speech(True)
            
    elif "turn the light back on" in action and memory["light"] == "off":
        hue.turn_on(LIGHT_ID)
        memory["light"] = "on"
        speak("The light has been turned back on.")
        if memory.get("music", True):
            music_player.resume_music()
        
        
    elif "turn the light back off" in action and memory["light"] == "on":
        hue.turn_off(LIGHT_ID)
        memory["light"] = "off"
        speak("The light has been turned back off.")
        if memory.get("music", True):
            music_player.resume_music()
        

    else:
        # Handle general queries
        if memory["last_response"]:
            response = get_openai_response(f"Given your last response: {memory["last_response"]}. {user_input}")
        response = get_openai_response(user_input)
        speak(response)
        memory["last_response"] = response
        if memory.get("music", True):
            music_player.resume_music()
        
    
        
        

def start_music_player(query):
    music_player.play_music(query)

def main():
    speak("Hello, I am JARVIS.")

    
    while True:
        user_input = recognize_speech(listen_for_wake_word=True)  
        user_input_lower = user_input.lower().replace("bike", "motorcycle")

        if any(phrase in user_input_lower for phrase in ["nevermind", "cancel", "shut up", "quiet", "never mind"]):
            prompt = f"I'm done talking to you. {user_input_lower}."
            response = get_openai_response(prompt)
            speak(response)
            if memory.get("music", True):
                music_player.resume_music()
            continue

        # Process the user input for intents
        process_command(user_input_lower)

        # Listening for potential follow-up questions
        print("Listening for potential follow-up questions for 10 seconds...")
        end_time = time.time() + 10  # Set listening duration
        while time.time() < end_time:
            follow_up_input = recognize_speech(listen_for_wake_word=False)  
            if follow_up_input:
                process_command(follow_up_input.lower())
                end_time = time.time() + 10  # Reset the timer

        print("Back to listening for the wake word...")

if __name__ == "__main__":
    main()
