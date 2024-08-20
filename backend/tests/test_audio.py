import unittest
from unittest.mock import MagicMock
import hashlib

from models.audio import Audio

class AudioTests(unittest.TestCase):
    def setUp(self):
        self.audio_file = "/path/to/audio.wav"
        self.whisper_model = "base"
        self.audio = Audio(self.audio_file, self.whisper_model)

    def test_get_file_name_path_with_folders(self):
        file_path = "/path/to/audio.wav"
        expected_file_name = "audio.wav"
        actual_file_name = self.audio.get_file_name(file_path)
        self.assertEqual(actual_file_name, expected_file_name)

    def test_get_file_name_path_without_folders(self):
        file_path = "audio.wav"
        expected_file_name = "audio.wav"
        actual_file_name = self.audio.get_file_name(file_path)
        self.assertEqual(actual_file_name, expected_file_name)

    def test_get_audio_id(self):
        file_name = "audio.wav"
        expected_id = hashlib.md5(file_name.encode()).hexdigest()
        actual_id = self.audio.get_id(self.audio_file)
        self.assertEqual(actual_id, expected_id)
        self.assertIsInstance(expected_id, str, "The ID is not a string")

    def test_is_valid_no_stream(self):
        probe_mock = MagicMock()
        probe_mock.return_value = {}

        with unittest.mock.patch("ffmpeg.probe", probe_mock):
            self.assertFalse(self.audio.is_valid())
    
    def test_is_valid_long_audio(self):
        probe_mock = MagicMock()
        probe_mock.return_value = {
            "streams": [
                {
                    "index": 0,
                    "codec_name": "opus",
                    "codec_type": "audio",
                    "duration": "120.282167"
                }
            ]
        }

        with unittest.mock.patch("ffmpeg.probe", probe_mock):
            self.assertFalse(self.audio.is_valid())

    def test_is_valid_no_audio_stream(self):
        probe_mock = MagicMock()
        probe_mock.return_value = {
            "streams": [
                {
                    "index": 0,
                    "codec_name": "h264",
                    "codec_type": "video",
                    "duration": "45.282167"
                }
            ]
        }

        with unittest.mock.patch("ffmpeg.probe", probe_mock):
            self.assertFalse(self.audio.is_valid())
    
    def test_is_valid_success(self):
        probe_mock = MagicMock()
        probe_mock.return_value = {
            "streams": [
                {
                    "index": 0,
                    "codec_name": "opus",
                    "codec_type": "audio",
                    "duration": "45.282167"
                }
            ]
        }

        with unittest.mock.patch("ffmpeg.probe", probe_mock):
            self.assertTrue(self.audio.is_valid())

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

        with unittest.mock.patch("models.audio.whisper", whisper_module_mock):
            expected_result = {
                "text": "Hello, world!",
                "language": "en",
                "length": 10
            }
            self.assertIsNone(self.audio.transcribed_at)
            actual_result = self.audio.transcribe()
            self.assertEqual(actual_result, expected_result)
            self.assertEqual(self.audio.text, expected_result["text"])
            self.assertEqual(self.audio.language, expected_result["language"])
            self.assertEqual(self.audio.length, expected_result["length"])
            self.assertIsNotNone(self.audio.transcribed_at)

    def test_to_dict(self):
        audio_dict = self.audio.to_dict()
        self.assertIsInstance(audio_dict, dict)
        self.assertEqual(5, len(audio_dict.keys()))
        self.assertIn("id", audio_dict)
        self.assertIn("text", audio_dict)
        self.assertIn("language", audio_dict)
        self.assertIn("length", audio_dict)
        self.assertIn("transcribed_at", audio_dict)
        