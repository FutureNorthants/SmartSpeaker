import speech_recognition as sr
import http.client
import json
import pyaudio
import time

# Setting up pretty printer - for debugging
# use like pp.pprint(message)
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Bringing in QnA connection details
from credentials import credentials
creds = credentials()

# Setting up text to speech
from gtts import gTTS
import os
speechlanguage = 'en'
speechRate = 0.75


# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
source = sr.Microphone()
#hot_word='Norbert'

def listen():
    with sr.Microphone() as source:
        #r.energy_threshold = 50
        r.dynamic_energy_threshold = True
        print("Talk")
        say ("How can I help you today?")
        time.sleep(1.5)
        audio_text = r.listen(source)
        print("finished listening")
        say ("thanks, looking for an answer...")
    try: 
        message = r.recognize_google(audio_text)
        return message
	 # if hot_word in message:
           # return message
    except sr.UnknownValueError:
        print("Could not understand audio")
    except IndexError:
            print("No internet connection")
            return 'error'
    except KeyError:
        print("Invalid API key or quota maxed out")
        return 'error'
    except LookupError:
        print("Could not understand audio")
        return 'error'


def get_QnA_results(statement, debug = False):
    statement = statement.replace("'", "")
    conn = http.client.HTTPSConnection(creds.QnA_DOMAIN)
    payload = "{'question':\'" + statement + "\'}"
    headers = {
        'Authorization': creds.QnA_AUTH,
        'Content-Type': 'application/json',
        'Cookie': creds.QnA_COOKIE
    }
    try:  
        conn.request("POST", creds.QnA_ENDPOINT, payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        formatted_response = json.loads(data)
        if debug == True: pp.pprint(formatted_response)
        if formatted_response['answers'][0]['score'] >= creds.QnA_CONFIDENCE:
            response = formatted_response['answers'][0]['answer']
        else:
            response = 'I couldn\'t find an answer for that, please add this to my database brain'

        return response
    except:
        print('Error connecting to QnA service')
        return ('error')
    

def say(statement):
    myobj = gTTS(text=statement, lang=speechlanguage, slow=False)
    myobj.save("norbert.mp3")
    os.system("mpg123 norbert.mp3")

def main():
    question = listen()
    if question != 'error':
        answer = get_QnA_results(question)
    if answer != 'error':
        say(answer)

main()

# print(listen())
# print (get_QnA_results("There's a broken Street Light in Kettering", True))
# say('I am a teapot, short and stout.')
