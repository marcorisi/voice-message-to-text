import logging
from flask import Flask, request, jsonify
from models.audio import Audio
from db import DB

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_request(request, status_code, operation):
    """
    Logs the details of a request.

    Parameters:
    - request (werkzeug.local.LocalProxy): The request object to log.
    - status_code (int): The status code of the response.
    - operation (str): The operation performed.

    Returns:
    - None
    """
    logging.info(f"{request.method} {request.path} - Status Code: {status_code} - Operation: {operation}")

@app.route('/ping', methods=['GET'])
def index():
    return 'pong'

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
        log_request(request, 200, "Audio already transcribed, returning existing record")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
    
    my_audio = Audio(file_name)
    my_audio.transcribe()
    db.insert_audio(my_audio)

    response = jsonify(my_audio.to_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    log_request(request, 201, "New audio transcribed, returning new record")
    return response, 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
