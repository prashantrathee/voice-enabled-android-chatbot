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
    '''
    API route to receive audio from the client-side, save it, convert it to FLAC format, 
    recognize speech from the audio and predict the response using skii. 
    Finally, returns the response to the client-side.
    '''
    if request.data:
        recognizer = sr.Recognizer()
        audio_mp3 = "audio.mp3"
        audio_pcm = "audio_input.pcm"
        
        # Saving the received audio as binary data to a file
        with open("audio_input.pcm", 'wb') as file:
            file.write(request.data)
        
        audio_flac = "audio_output.flac"
        
        # Converting the saved audio file to FLAC format to be used by the recognizer
        subprocess.run(["ffmpeg", "-y", "-i","audio_input.pcm","-ar","8000", "-ac", "1", "-f","wav", "temp.wav"],shell=True,check=True)
        subprocess.run(["sox","temp.wav","-C", "0", "audio_output.flac"],shell=True,check=True)

        # Recognizing the speech from the audio using the recognizer
        with sr.AudioFile(audio_flac) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        print("Recognized text = ", text)

        # Predicting the response from skii
        skii_object = skii()
        result = skii_object.predict(text)

        # Creating the response to be sent back to the client-side
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
    '''
    API route to receive query from the client-side, predict the response using skii and 
    return the response to the client-side.
    '''
    skii_object = skii()
    query = request.args.get('query')
    result = skii_object.predict(query)

    # Creating the response to be sent back to the client-side
    response = {
        'message': result,
        'fromSender': False,
        'fromSkii': True
    }
    return response, 200


def get_response(message):
    '''
    Function to get response from skii using the given message.
    '''
    skii_object = skii()
    result = skii_object.predict(message)
    return result


def runInTerminal():
    '''
    Function to run the program in terminal by taking user input and returning the response from skii.
    '''
    while True:
        message = input("")
        print(get_response(message))


def print_hi(name):
    '''
    Function to print a message with the given name.
    '''
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='192.168.201.100', port=1578)
    # sendAudio()
    # runInTerminal()
