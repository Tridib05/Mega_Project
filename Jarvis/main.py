import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai 
#from gtts import gTTS
#import pygame
#import os
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="3d050a0821ad4c7ea44be62b52d1cfdb"
def speak(text):
    engine.say(text)
    engine.runAndWait( )
'''
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize the mixer
    pygame.mixer.init()
    # Load your MP3 file
    pygame.mixer.music.load('temp.mp3')  
    # Play the music
    pygame.mixer.music.play()
    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(0.1)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
'''
def aiprocess(command):
    genai.configure(api_key="AIzaSyCFpRJSroVzLN3Ik_AEBFl1OJsrfUf8biM")
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(command)
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com") 
    elif "open firefox" in c.lower():
        webbrowser.open("https://firefox.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=3d050a0821ad4c7ea44be62b52d1cfdb")
        #Parse the JSON response
        data = r.json()
        if data["status"] == "ok":
            print("Top US Headlines:\n")
            for i, article in enumerate(data["articles"]):
                speak(f"{i+1}. {article['title']}")
    else: 
        #Let genai handle the request
        output = aiprocess(c)
        speak(output)
    
if __name__== '__main__':
    speak("Initializing Jarvis....")
    while True:
        #Listen for the wake word "Jarvis"
        #obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Yes,how can I help?")
                #Listen for command
                with sr.Microphone() as source:
                    print("jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))