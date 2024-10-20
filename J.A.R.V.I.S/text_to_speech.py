import time
import pygame
from google.cloud import texttospeech
from config import GOOGLE_API_KEY

def speak(text):
    # Set up the client with the credentials
    client = texttospeech.TextToSpeechClient.from_service_account_json('jarvis-439022-4d1ff61a47ab.json')
    
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Build the voice request, select the language code and voice type (robotic)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-GB-News-M",  # Choose a voice that fits your needs
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Change to FEMALE if desired
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=.7,
        speaking_rate=.8,
        volume_gain_db=0,   
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the response to an MP3 file
    audio_file = "speech.mp3"  # Define the MP3 file path
    with open(audio_file, "wb") as out:
        out.write(response.audio_content)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load(audio_file)

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():  # Keep looping until the music is done playing
        time.sleep(0.1)  # Sleep a bit to avoid busy waiting

    # Optionally, stop the mixer
    pygame.mixer.quit()
