# main.py - Jarvis Voice Assistant
# Functionality summary:
# - speak(text): Speaks text using gTTS and pygame
# - aiprocess(command): Uses Gemini AI to generate a response
# - processCommand(c): Handles user commands (open sites, play music, news, or AI)
# - Main loop: Listens for wake word 'Jarvis', then listens for a command and processes it

import speech_recognition as sr                 # For speech recognition
import webbrowser                               # For opening web pages
import pyttsx3                                  # For TTS (not used in final speak)
import musiclibrary                             # Custom music links
import requests                                 # For news API
import google.generativeai as genai             # For Gemini AI

from gtts import gTTS                           # For Google TTS
import pygame                                   # For playing mp3
import os                                       # For file operations

recognizer = sr.Recognizer()   # Initialize speech recognizer
engine = pyttsx3.init()    # Initialize TTS engine                
newsapi="Your Api key"                                  

def speak(text):
    """
    Speaks the given text using pyttsx3 (offline, fast).
    """
    engine.say(text)
    engine.runAndWait()

def speak(text):                
    """
    Speaks the given text using gTTS and pygame.
    """
    tts = gTTS(text)                            
    tts.save('temp.mp3')                             
    pygame.mixer.init()             
    pygame.mixer.music.load('temp.mp3')          
    pygame.mixer.music.play()           
    while pygame.mixer.music.get_busy():            
        pygame.time.Clock().tick(0.1)           
    pygame.mixer.music.unload()         
    os.remove("temp.mp3")  
     

def aiprocess(command):
    """     
    Sends the command to Gemini AI and returns the response text.
    """
    genai.configure(api_key="")      
    model = genai.GenerativeModel("gemini-2.5-flash")           
    response = model.generate_content(command)              
    return response.text                

def processCommand(c):
    """
    Processes the user's command: opens websites, plays music, fetches news, or uses AI for other queries.
    """
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
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi")
        data = r.json()
        if data["status"] == "ok":
            print("Top US Headlines:\n")            
            for i, article in enumerate(data["articles"]):      
                speak(f"{i+1}. {article['title']}")         
    else: 
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
