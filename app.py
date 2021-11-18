import speech_recognition as sr
import http.client
import json

# Setting up pretty printer - for debugging
# use like pp.pprint(message)
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Bringing in QnA connection details
from credentials import credentials
creds = credentials()

# Setting up text to speach
import pyttsx3
engine = pyttsx3.init()

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

def listen():
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    # Sends the audio clip to google for transcription
    # todo: Look into setting up own google api key and store in credentials
    # // Have it listen at the start to gauge backgroud noise
    # // todo: Maybe set max duration and / or dynamically determine noise levels
    with sr.Microphone() as source:
        print('Getting ambient noise levels')
        r.adjust_for_ambient_noise(source, 0.5)
        r.dynamic_energy_threshold = True

        print("Talk")
        audio_text = r.listen(
            source, 
            phrase_time_limit=10, 
            )
        print("Time over, thanks") 

        try: 
            message = r.recognize_google(
                audio_text, 
                language='en-gb',
                # key=None,
                )
            return message
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
            response = 'I couldn\'t find an answer for that, please try searching the website'

        return response
    except:
        print('Error connecting to QnA service')
        return ('error')
    

def say(statement):
    engine.say(statement)
    engine.runAndWait()


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