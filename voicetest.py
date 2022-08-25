'''import pyttsx3
import gTTS
gtts-cli 'hello' --output hello.mp3'''

'''import picospeaker'''
'''from decouple import config'''

'''USERNAME = config('USER')
BOTNAME = config('BOTNAME)'''


'''engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    
    engine.say(text)
    engine.runAndWait()'''

'''engine = picospeaker.init()
engine.setProperty("rate",125)
engine.setProperty("voice","english+f4")
engine.say("How much wood could a woodchuck chuck if a woodchuck could chuck wood")
engine.runAndWait()
engine.stop()
voices = engine.getProperty("voices")'''
'''print("Number of voices: ",len(voices))
for voice in voices:
	print (voice, voice.id)
	engine.setProperty("voice", voice.id)
	engine.say("How much is that doggy in the window")
	engine.runAndWait()
	engine.stop()'''
# Import the required module for text 
# to speech conversion
from gtts import gTTS
  
# This module is imported so that we can 
# play the converted audio
import os
  
# The text that you want to convert to audio
mytext = 'Welcome to geeksforgeeks!'
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome 
myobj.save("welcome.mp3")
  
# Playing the converted file
os.system("mpg123 welcome.mp3")

