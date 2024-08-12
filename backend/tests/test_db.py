import unittest
import os
from unittest.mock import MagicMock
from tinydb import Query
from db import DB

class DBTests(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_db.json"
        self.db = DB(self.db_name)

    def test_get_existing_audio(self):
        audio_id = 123
        audio_record = {"id": audio_id, "text": "Hello, world!", "language": "en", "length": 10}
        self.db.db.insert(audio_record)

        expected_result = audio_record
        actual_result = self.db.get(audio_id)
        self.assertEqual(actual_result, expected_result)

    def test_get_nonexistent_audio(self):
        audio_id = 123
        actual_result = self.db.get(audio_id)
        self.assertIsNone(actual_result)

    def test_insert_audio(self):
        audio = MagicMock()
        audio.to_dict.return_value = {"text": "Hello, world!", "language": "en", "length": 10}

        expected_id = 1
        actual_id = self.db.insert_audio(audio)
        self.assertEqual(actual_id, expected_id)

        audio_record = self.db.db.get(doc_id=expected_id)
        self.assertIsNotNone(audio_record)
        self.assertEqual(audio_record["text"], "Hello, world!")
        self.assertEqual(audio_record["language"], "en")
        self.assertEqual(audio_record["length"], 10)

    def test_get_all(self):
        audio_records = [
            {"text": "Hello, world!", "language": "en", "length": 10},
            {"text": "Bonjour le monde!", "language": "fr", "length": 15},
            {"text": "Hola, mundo!", "language": "es", "length": 12}
        ]
        for audio_record in audio_records:
            self.db.db.insert(audio_record)

        expected_result = audio_records
        actual_result = self.db.get_all()
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(3, len(actual_result))
    
    def test_truncate(self):
        audio_records = [
            {"text": "Hello, world!", "language": "en", "length": 10},
            {"text": "Bonjour le monde!", "language": "fr", "length": 15},
            {"text": "Hola, mundo!", "language": "es", "length": 12}
        ]
        for audio_record in audio_records:
            self.db.db.insert(audio_record)

        all_items = self.db.get_all()
        self.assertEqual(3, len(all_items))
        self.db.truncate()
        all_items = self.db.get_all()
        self.assertEqual(0, len(all_items))
        self.assertEqual([], all_items)
    
    def tearDown(self):
        self.db.db.close()
        os.remove(self.db_name)
