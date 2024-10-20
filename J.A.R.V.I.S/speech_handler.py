import speech_recognition as sr
from text_to_speech import speak
from config import GOOGLE_API_KEY
import pygame
import time
import threading
import music_player

listen_for_wake_word = True
recognizer = sr.Recognizer() # Initialize Recognizer

def listen_for_the_wake_word(source):
    print("Listening for wake word...")  
    while True:
        try:
            audio = recognizer.listen(source, timeout=30)
            command = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_API_KEY)
            if "jarvis" in command.lower():
                
                if music_player.is_music_playing:
                    print("Wake word detected. Pausing music...")
                    music_player.pause_music()
                    
                pygame.mixer.init()
                sound = pygame.mixer.Sound('subtle.mp3')
                sound.set_volume(.15)
                sound.play()
                pygame.time.delay(1000)

                print("Wake word detected! Listening for your command...")
                    
                listen_for_wake_word = True
                return listen_for_wake_word
        except sr.WaitTimeoutError:
            #print("Going back to waiting for wake word.")
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Sorry, I couldn't reach the speech recognition service; {e}")

def recognize_speech(listen_for_wake_word):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        if listen_for_wake_word:
            while True:  # Keep looping until a valid command is received
                if listen_for_the_wake_word(source):
                    while True:  # Loop for recognizing the command after the wake word
                        try:
                            audio = recognizer.listen(source)
                            print("Audio received, processing...")
                            text = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_API_KEY)
                            return text  # Return the recognized command
                        except sr.UnknownValueError:
                            print("Sorry, I didn't catch that. Please repeat.")
                            continue  # Continue the loop to keep listening for the command
                        except sr.RequestError as e:
                            print(f"Sorry, I couldn't reach the speech recognition service; {e}")
                            break  # Exit the loop if there is a request error
        else:
            print("Waiting for command")
            unknown_count = 0
            while True:  # Loop until a valid command is received
                try:
                    recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
                    audio = recognizer.listen(source, timeout=10)
                    print("Audio received, processing...")
                    text = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_API_KEY)
                    unknown_count = 0
                    return text  # Return the recognized command
                except sr.WaitTimeoutError:
                    print("Going back to waiting for wake word.")
                    break  # Break out of this loop after restarting wake word detection
                except sr.UnknownValueError:
                    print("Sorry, I didn't catch that. Please repeat.")
                    unknown_count += 1
                    if unknown_count >= 3:  # Check if there have been 3 consecutive failures
                        print("Too many failed attempts. Going back to waiting for wake word.")
                        break  # Exit and go back to wait for the wake word
                    continue  # Continue the loop to keep listening for the command
                except sr.RequestError as e:
                    print(f"Sorry, I couldn't reach the speech recognition service; {e}")
                    break  # Exit the loop if there is a request error