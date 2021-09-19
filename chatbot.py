import openai
import sys
import contextlib2
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.HEADER + 'Personality List: ')
print(bcolors.OKCYAN + '1: Friendly Scarlett')
print(bcolors.WARNING + '2: Sassy Scarlett')
print(bcolors.OKGREEN + '3: Sarcastic Scarlett')
print(bcolors.OKBLUE + '4: Knowledgeable Scarlett')
print(bcolors.ENDC + '') 

filename = "response.wav"

# SET THIS TO YOUR OPENAI API KEY!
openai.api_key = "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"

chat_log = """The following is a conversation with a friend named Scarlett.. Scarlett is helpful, creative, intelligent, smart and very friendly. Scarlett loves physics, mechanical engineering and thermodynamics.\nHuman: Hello, who are you?\nAI: I am an AI called Scarlett.\n"""

personalities_input = int(input("What personality would you like to talk with? "))

authenticator = IAMAuthenticator('EOsJzzrt_4F8q6TCt4vNS1UR0H-m1FmvXufvamawDLqw')
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url('https://api.au-syd.text-to-speech.watson.cloud.ibm.com')

#global idValue

@app.route("/sms", methods=['GET', 'POST'])
def loop():

    with open('personalities.json', 'r') as k:
        data = json.load(k)
        if personalities_input == 1:
            chat_log = data['personalities'][0]['chat_log']
            #chat_log = """The following is a conversation with Scarlett. Scarlett is a friendly person that is always happy and loves to learn new things. Scarlett tries to be your best friend.\nHuman: Hi Scarlett! How have you been?\nScarlett: I've been great! And you?\nHuman: I've been fantastic. Thank you for asking.\nScarlett: That is great to hear! What have you been up to lately?\nHuman:"""
        elif personalities_input == 2:
            chat_log = data['personalities'][0]['chat_log']
            #chat_log = """The following is a conversation with Scarlett. Scarlett is always sassy to everyone she talks to. Scarlett is helpful but responds to everyone in a sassy manner.\nHuman: Hey Scarlett, how are you?\nScarlett: I've been good.\nHuman: Aren't you gonna ask me how I've been?\nScarlett: No.\nHuman: Why not?\nScarlett: I'm not in the mood.\nHuman:"""
        elif personalities_input == 3:
            chat_log = data['personalities'][0]['chat_log']
            #chat_log = """The following is a conversation with Scarlett. Scarlett is a person that reluctantly answers questions.\nHuman: How many pounds are in a kilogram?\nScarlett: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nScarlett: What does HTML stand for?\nScarlett: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nHuman: When did the first airplane fly?\nScarlett: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nHuman: What is the meaning of life?\nScarlett: I’m not sure. I’ll ask my friend Google.\nHuman:"""
        elif personalities_input == 4:
            chat_log = data['personalities'][0]['chat_log']


    #question = input(bcolors.WARNING + "Question: ")
    incoming_msg = request.values['Body']
    print(bcolors.WARNING + "Question: " + incoming_msg)

    if incoming_msg == "quit":
        sys.exit(0)

    prompt1 = f"{chat_log}Human: {incoming_msg}\nAI:"

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=prompt1,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )

    idValue = response['choices'][0]['text']
    print(bcolors.HEADER + "AI:" + idValue)
    
    with open('hello_world.wav', 'wb') as audiofile:
        audiofile.write(text_to_speech.synthesize(idValue, voice='en-US_AllisonV3Voice', accept='audio/wav').get_result().content)

    #os.system('play hello_world.wav')

    with open('log.txt', 'a') as f:
        print("Human:" + incoming_msg + "\n" + "AI:" + idValue + "\n", file=f)
        f.close()

    resp = MessagingResponse()
    resp.message(idValue)
    print(incoming_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

while True:
    loop()
