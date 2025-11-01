from pathlib import Path
from base64 import encode
from email.utils import quote
import json
import os
import re
import struct
import subprocess
import time
import requests
from hugchat import hugchat
import pvporcupine
import pyaudio
import pyautogui
import engine
import webbrowser
from playsound import playsound
import eel
from engine.db import sqlite3
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
from dotenv import load_dotenv
from engine.helper import extract_yt_term, remove_words
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, 'envjarvis', '.env'))

GROK_KEY = os.getenv('GROK_KEY')

conn = sqlite3.connect("ewil.db")
cursor = conn.cursor()
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

         try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
         except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)



def playSpotify(query):
    speak("Opening Spotify...")

    # remove assistant words
    for word in ["play", "on spotify", "spotify", "jarvis"]:
        query = query.replace(word, "")

    song = query.strip()

    # find spotify actual exe
    os.startfile("spotify")

    # open spotify
    #subprocess.Popen(spotify_path)
    #time.sleep(3)  # wait for Spotify to open

    if song == "":
        return
    
    speak(f"Searching and playing {song}")

    # focus search bar in Spotify
    pyautogui.hotkey("ctrl", "l")   # Spotify search shortcut
    time.sleep(0.5)
    pyautogui.typewrite(song, interval=0.07)
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(2)

    # Press enter again to play first result
    pyautogui.press("enter")


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["ewil","evil","jarvis"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    


def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 20
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 13
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

  # If you have it, else leave empty

def generate_reply_with_grok(prompt):
    # If no key, skip
    if not GROK_KEY:
        return None
    try:
        # This is just a fallback message style
        # acting like Grok is answering
        reply = f"✦ (GROK Response Fallback) → {prompt}? Interesting. But I currently don't have access to the live Grok API."
        return reply

    except Exception as e:
        print("[Grok Error]", e)
        return None


def chatBot(query):
    user_input = query.lower()

    # 1) Try HuggingFace first
    try:
        from hugchat import hugchat
        chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print("HF Response:", response)
        speak(response)
        return response

    except Exception as e:
        print("[HuggingFace Error]", e)

    # 2) Then fallback to Grok-style response
    response = generate_reply_with_grok(user_input)
    if response:
        print("Grok Style Response:", response)
        speak(response)
        return response

    # 3) If both fail
    fallback = "I'm experiencing network or API issues right now, boss."
    print("Fallback:", fallback)
    speak(fallback)
    return fallback
    
