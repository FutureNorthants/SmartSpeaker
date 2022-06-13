import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate",125)
engine.setProperty("voice","english+f4")
engine.say("How much wood could a woodchuck chuck if a woodchuck could chuck wood")
engine.runAndWait()
engine.stop()
voices = engine.getProperty("voices")
'''print("Number of voices: ",len(voices))
for voice in voices:
	print (voice, voice.id)
	engine.setProperty("voice", voice.id)
	engine.say("How much is that doggy in the window")
	engine.runAndWait()
	engine.stop()'''

