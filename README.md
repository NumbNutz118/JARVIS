# JARVIS AI Home Assistant

**JARVIS AI Home Assistant** is a personal voice-controlled assistant that mimics the personality of JARVIS from the movies, featuring dry humor and sarcasm. It can provide general information, deliver local weather updates, control smart home lighting, and play music, all through natural voice interactions.

## Features

- **General Information**: Get responses to common inquiries, enhanced with JARVIS-like humor.
- **Weather Updates**: Fetch the current weather and 1-day forecast based on your location.
- **Smart Light Control**: Control your Philips Hue lights by turning them on/off and adjusting brightness.
- **Music Playback**: Request a song by voice, and JARVIS will play it for you using the YouTube Music API.

## Requirements

- Python 3.x
- Raspberry Pi (Zero 2 W or similar)
- Microphone and speakers (e.g., ReSpeaker 2-Mic Pi HAT, Creative Pebble 2.0)
- Philips Hue lights and bridge
- Google Cloud Speech Recognition (for speech recognition) or alternative speech recognition system
- Google API key for text-to-speech functionality
- WeatherAPI API key for weather and forecast information
- YouTube Music API for song playback

## Usage

Start the JARVIS AI system:

```bash
python main.py
```
Once activated, say "Jarvis" to wake the assistant. It will acknowledge with a subtle sound and be ready for commands.

### Example Commands:
* Weather:
  * "What's the weather like?"
  * "Will it rain tomorrow?"
* Lighting:
  * "Turn on the lights."
  * "It's a little bright in here." (JARVIS will dim the lights)
  * "Turn off the lights."
* Music:
  * "Play Call Me Little Sunshine by Ghost."
  * "Pause the music."

## Known Issues
- May struggle with commands in noisy environments. Consider using a more advanced microphone setup.
- Sometimes misunderstands ambiguous commands. Use clear phrasing for best results.

## Future Improvements
- Extend the system to control more smart devices.
- Incorporate more natural language understanding to make conversations smoother.
