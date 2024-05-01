from flask import Flask, request, jsonify
from audio import Audio
from db import DB

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_file = request.files['audio']
    file_name = f"storage/{audio_file.filename}"
    audio_file.save(file_name)

    my_audio = Audio(file_name)
    result = my_audio.transcribe()

    db = DB()
    db.insert_audio(my_audio)

    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200
    