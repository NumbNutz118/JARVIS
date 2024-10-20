import os
import time
import pygame
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
import threading
from ytmusicapi import YTMusic

audio_file = None
mp3 = None
is_music_playing = False  # Global flag for music state
lock = threading.Lock()   # Thread lock to handle state changes safely
start_time = None
duration = 0  # Initialize duration

def ensure_mixer_initialized():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

def convert_mp4_to_mp3(mp4_file, mp3_file):
    video_clip = VideoFileClip(mp4_file)
    video_clip.audio.write_audiofile(mp3_file)
    video_clip.close()
    return mp3_file

def play_music_player(url, action='play'):
    global is_music_playing, audio_file, mp3, start_time, duration
    
    if action == 'play':
        yt = YouTube(url)
        stream = yt.streams.first()
        audio_file = stream.download(filename="audio.mp4")

        mp3 = convert_mp4_to_mp3(audio_file, "audio.mp3")

        ensure_mixer_initialized()  # Ensure the mixer is initialized before playing
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()
        start_time = time.time()
        is_music_playing = True  # Set flag to true when music starts

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        is_music_playing = False  # Reset flag when music ends

    elif action == 'pause':
        with lock:
            ensure_mixer_initialized()  # Ensure the mixer is initialized before pausing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                duration = time.time() - start_time
                is_music_playing = False  # Update the flag appropriately
                print("Music paused.")

    elif action == 'resume':
        with lock:
            ensure_mixer_initialized()  # Ensure the mixer is initialized before resuming
            pygame.mixer.music.load("audio.mp3")
            pygame.mixer.music.play(start=duration)
            start_time = time.time() - duration
            is_music_playing = True
            print("Music resumed.")
            

    elif action == 'stop':
        with lock:
            ensure_mixer_initialized()  # Ensure the mixer is initialized before stopping
            pygame.mixer.music.stop()
            is_music_playing = False  # Reset flag
            print("Music stopped.")
            if audio_file:
                os.remove(audio_file)

def play_music(query):
    ytmusic = YTMusic("oauth.json")
    search_results = ytmusic.search(query, limit=1)
    first_result = search_results[0]

    for key, value in first_result.items():
        if key == 'videoId':
            top_result_video_id = value

    play_music_player('https://www.youtube.com/watch?v=' + top_result_video_id, action='play')

def pause_music():
    play_music_player(None, action='pause')

def resume_music():
    play_music_player(None, action='resume')

def stop_music():
    play_music_player(None, action='stop')
