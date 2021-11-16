#import library
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
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks") 
        try: # recognize__() method will throw a request error if the API is unreachable, hence using exception handling
            message = r.recognize_google(audio_text) # using google speech recognition
            print("Text: "+ message)
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


# Reading Microphone as source
# listening the speech and store in audio_text variable
def main():
    question = listen()
    if question != 'error':
        answer = get_QnA_results(question)
    if answer != 'error':
        say(answer)

main()

# print (get_QnA_results("There's a broken Street Light in Kettering", True))