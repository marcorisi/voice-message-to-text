import whisper

class Audio:
    """
    Represents an audio file and provides methods for transcription.
    """

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
        return {
            "text": result['text'],
            "language": result['language'],
            "length": self.get_audio_length(result)
        }