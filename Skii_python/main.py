
import os.path
import wave
import subprocess

import flask
from flask import request
import speech_recognition as sr

import skii
from skii import *

app = flask.Flask(__name__)


@app.route("/sendAudio", methods=['POST'])
def sendAudio():
    flag = True
    if request.data:
        recognizer = sr.Recognizer()
        audio_mp3 = "audio.mp3"
        audio_pcm = "audio_input.pcm"
        with open("audio_input.pcm", 'wb') as file:
            file.write(request.data)
        audio_flac = "audio_output.flac"
        subprocess.run(["ffmpeg", "-y", "-i","audio_input.pcm","-ar","8000", "-ac", "1", "-f","wav", "temp.wav"],shell=True,check=True)
        subprocess.run(["sox","temp.wav","-C", "0", "audio_output.flac"],shell=True,check=True)
        # subprocess.run(cmd, shell=True, check=True)
        with sr.AudioFile(audio_flac) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        print("Recognized text = ", text)
        skii_object = skii()
        result = skii_object.predict(text)
        response = [
        {
            'message':text,
            'fromSender':True,
            'fromSkii':False
        },
        {
            'message': result,
            'fromSender': False,
            'fromSkii': True
        }]
        return response,200



@app.route('/send_query', methods=['GET'])
def send_query():
    # query = request.json
    print("got query here")
    skii_object = skii()
    query = request.args.get('query')
    result = skii_object.predict(query)
    response = {
        'message': result,
        'fromSender': False,
        'fromSkii': True
    }
    return response, 200


def get_response(message):
    skii_object = skii()
    result = skii_object.predict(message)
    return result


def runInTerminal():
    while True:
        message = input(">")
        print(get_response(message))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # app.run(host='192.168.69.64', port=1578)
    # sendAudio()
    print_hi("Prashant")
    runInTerminal()
