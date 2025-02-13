import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")


import pyttsx3

engine = pyttsx3.init()
engine.say("Hello, how can I help you?")
engine.runAndWait()
