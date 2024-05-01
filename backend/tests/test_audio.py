import unittest
from unittest.mock import MagicMock

from audio import Audio

class AudioTests(unittest.TestCase):
    def setUp(self):
        self.audio_file = "/path/to/audio.wav"
        self.whisper_model = "base"
        self.audio = Audio(self.audio_file, self.whisper_model)

    def test_get_audio_length(self):
        whisper_transcribe_result = {
            "segments": [
                {"start": 0, "end": 5},
                {"start": 5, "end": 10}
            ]
        }
        expected_length = 10
        actual_length = self.audio.get_audio_length(whisper_transcribe_result)
        self.assertEqual(actual_length, expected_length)

    def test_transcribe(self):
        model_mock = MagicMock()
        model_mock.transcribe.return_value = {
            "text": "Hello, world!",
            "language": "en",
            "segments": [
                {"start": 0, "end": 5},
                {"start": 5, "end": 10}
            ]
        }
        whisper_load_model_mock = MagicMock(return_value=model_mock)
        whisper_module_mock = MagicMock()
        whisper_module_mock.load_model = whisper_load_model_mock

        with unittest.mock.patch("audio.whisper", whisper_module_mock):
            expected_result = {
                "text": "Hello, world!",
                "language": "en",
                "length": 10
            }
            actual_result = self.audio.transcribe()
            self.assertEqual(actual_result, expected_result)