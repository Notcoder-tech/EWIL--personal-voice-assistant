import os
import eel
from engine.features import *
from engine.command import *
import threading

def start():
    

    eel.init('www')

    #playAssistantSound()
    def play_startup_sound():
        path = r"D:\\JARVIS\\www\\assets\\audio\\start_sound.mp3"
        threading.Thread(target=playsound, args=(path,), daemon=True).start()


    play_startup_sound()
    eel.start("index.html", mode="edge", host="localhost", block=True)
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)

