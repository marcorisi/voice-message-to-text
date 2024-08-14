import whisper
import hashlib
from datetime import datetime

class Audio:
    """
    Represents an audio file and provides methods for transcription.
    """

    @staticmethod
    def get_file_name(file_path):
        """
        Gets the name of the file from the file path.

        Parameters:
        - file_path (str): The path to the audio file.

        Returns:
        - str: The name of the file.
        """
        return file_path.split('/')[-1]
    
    @staticmethod
    def get_id(file_path):
        """
        Gets the ID of the audio file.
        The ID is generated by MD5 hashing the file name.
        I used the MD5 algo as it is fast and secure enough for this use case.

        Parameters:
        - file_path (str): The path to the audio file.

        Returns:
        - str: The ID of the audio file.
        """
        file_name = __class__.get_file_name(file_path)
        return hashlib.md5(file_name.encode()).hexdigest()
        

    def __init__(self, audio_file, whisper_model='base'):
        """
        Initializes an Audio object.

        Parameters:
        - audio_file (str): The path to the audio file.
        - whisper_model (str): The name of the Whisper model to use for transcription.
                               Defaults to 'base'.
        """
        self.audio_file = audio_file
        self.whisper_model = whisper_model
        self.id = self.get_id(audio_file)
        self.text = None
        self.language = None
        self.length = None
        self.transcribed_at = None

    def get_audio_length(self, whisper_transcribe_result):
        """
        Calculates the length of the audio in seconds.

        Parameters:
        - whisper_transcribe_result (dict): The result of the Whisper transcription.

        Returns:
        - float: The length of the audio in seconds.
        """
        last_segment = whisper_transcribe_result['segments'][-1]
        return last_segment['end']
        
    def transcribe(self):
        """
        Transcribes the audio file using the Whisper model.

        Returns:
        - dict: A dictionary containing the transcribed text, language, and length of the audio.
        """
        model = whisper.load_model(self.whisper_model)
        result = model.transcribe(self.audio_file)

        self.text = result['text']
        self.language = result['language']
        self.length = self.get_audio_length(result)
        self.transcribed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "text": self.text,
            "language": self.language,
            "length": self.length
        }
    
    def to_dict(self):
        """
        Converts the Audio object to a dictionary that can be stored in the database.
        The returned dictionary contains only a few relevant properties (ID, ...)

        Returns:
        - dict: A dictionary representation of the Audio object.
        """
        PROPERTY_TO_KEEP = ["id", "text", "language", "length", "transcribed_at"]
        dict = self.__dict__
        return {key: dict[key] for key in PROPERTY_TO_KEEP}
