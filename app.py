#import library
import speech_recognition as sr
import http.client
import json

import pprint
# Setting up pretty printer - for debugging
# use like pp.pprint(message)
pp = pprint.PrettyPrinter(indent=4)

from credentials import credentials
creds = credentials()

#import pyttsx3
#engine = pyttsx3.init()


def listen():
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks") 
        try: # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            message = r.recognize_google(audio_text) # using google speech recognition
            print("Text: "+ message)
            return message
        except Exception as e:
            print("Sorry, I did not get that" + e)


def get_QnA_results(statement):
    conn = http.client.HTTPSConnection(creds.QnA_DOMAIN)
    payload = "{'question':'" + statement + "'}"
    headers = {
        'Authorization': creds.QnA_AUTH,
        'Content-Type': 'application/json',
        'Cookie': creds.QnA_COOKIE
    }

    conn.request("POST", creds.QnA_ENDPOINT, payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    formatted_response = json.loads(data)

    if formatted_response['answers'][0]['score'] >= creds.QnA_CONFIDENCE:
        response = formatted_response['answers'][0]['answer']
    else:
        response = 'I couldn\'t find an answer for that, please try searching the website'

    return response


def say(statement):
    engine.say(statement)
    engine.runAndWait()


# Reading Microphone as source
# listening the speech and store in audio_text variable
def main():
    question = listen()
    answer = get_QnA_results(question)
    say(answer)

#main()
print(listen())