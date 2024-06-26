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
    
    def tearDown(self):
        self.db.db.close()
        os.remove(self.db_name)