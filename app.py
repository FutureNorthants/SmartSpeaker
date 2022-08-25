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
import os.path 
speechlanguage = 'en'
speechRate = 0.75


# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
source = sr.Microphone()
#hot_word='Norbert'

def setup():
    if not os.path.exists('intro.mp3'):
        gTTS(text='How can I help you today', lang=speechlanguage, slow=False).save("intro.mp3")
    if not os.path.exists('looking.mp3'):
        gTTS(text='thanks, looking for an answer...', lang=speechlanguage, slow=False).save("looking.mp3")
    if not os.path.exists('no_internet.mp3'):
        gTTS(text='You have no internet connection. Speak with Ant or Megs', lang=speechlanguage, slow=False).save("no_internet.mp3")
        

def say_in_built(file):
    os.system('mpg321 '+file+'.mp3')
    
    

def listen():
    with sr.Microphone() as source:
        #r.energy_threshold = 50
        r.dynamic_energy_threshold = True
        print("Talk")
        say_in_built('intro')
        time.sleep(1.5)
        audio_text = r.listen(source)
        print("finished listening")
        say_in_built('looking')
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
    
def check_internet_connection():
    try:
        urllib.request.urlopen('http://www.google.com')
        return True
    except:
        return False

def main():
    if check_internet_connection():
        setup()
        question = listen()
        if question != 'error':
            answer = get_QnA_results(question)
        if answer != 'error':
            say(answer)

main()

# print(listen())
# print (get_QnA_results("There's a broken Street Light in Kettering", True))
# say('I am a teapot, short and stout.')
