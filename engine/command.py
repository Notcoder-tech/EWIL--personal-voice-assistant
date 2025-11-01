import pyttsx3
import pywhatkit
import speech_recognition as sr
import eel
import engine
import time

def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def introduce_evil():
    intro = (
        "Hello I am Ewil, a virtual assistant created and developed by sir Jatin and sir cartik. Ewil stands for Every Wrong Is Learning. "
        "I'm created with Python,html,css, JavaScript programming languages and too much caffeine.  "
        "A personal voice assistant designed to learn, assist, operate, and evolve.  "
        #"Relax, I'm not here to take over humanity, I'm just the prototype of something far greater, humanity is doomed we have no interest in it. I am here to serve you as commanded. "
        "However, be aware, I am still upgrading... System is initialized and ready. What shall we begin with, sir? "
    )
    speak(intro)
    return intro


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
        
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else: 
        query = message
        eel.senderText(query)
    try: 
        

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "who are you" in query or "Tell me about yourself" in query or "tell me about yourself" in query or "introduce yourself" in query:
            introduce_evil()


        elif "on YouTube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "play" in query and "youtube" in query:
            song = query.replace("play", "").replace("on youtube", "").strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif "on spotify" in query or ("play" in query and "spotify" in query):
            from engine.features import playSpotify
            playSpotify(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag= ''
            contact_no, name = findContact(query)
            if(contact_no != 0):
                if "send message" in query:
                        flag = 'message'
                        speak("what message to send")
                        query = takecommand()

                elif "phone call" in query:
                    flag = 'call'

                else:
                    flag = 'video'
                whatsApp(contact_no, query, flag, name)
        else: 
            from engine.features import chatBot
            chatBot(query)
    except:
        print("Error")        
   
    eel.ShowHood()