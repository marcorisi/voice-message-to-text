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

    # Look if you have already transcribed this audio
    db = DB()
    audio_id = Audio.get_id(file_name)
    audio_record = db.get(audio_id)
    if audio_record:
        response = jsonify(audio_record)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    
    my_audio = Audio(file_name)
    my_audio.transcribe()
    db.insert_audio(my_audio)

    response = jsonify(my_audio.to_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 201
    