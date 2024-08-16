import unittest
import os
from unittest.mock import MagicMock
from tinydb import Query
from db import DB

class DBTests(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_db.json"
        self.db = DB(self.db_name)
        self.audio_table = self.db.db.table(DB.AUDIO_TABLE)
        self.api_key_table = self.db.db.table(DB.API_KEY_TABLE)

    def test_get_existing_audio(self):
        audio_id = 123
        audio_record = {"id": audio_id, "text": "Hello, world!", "language": "en", "length": 10}
        self.audio_table.insert(audio_record)

        expected_result = audio_record
        actual_result = self.db.get_audio(audio_id)
        self.assertEqual(actual_result, expected_result)

    def test_get_nonexistent_audio(self):
        audio_id = 123
        actual_result = self.db.get_audio(audio_id)
        self.assertIsNone(actual_result)

    def test_insert_audio(self):
        audio = MagicMock()
        audio.to_dict.return_value = {"text": "Hello, world!", "language": "en", "length": 10, "transcribed_at": "2024-01-01 12:00:00"}

        expected_id = 1
        actual_id = self.db.insert_audio(audio)
        self.assertEqual(actual_id, expected_id)

        audio_record = self.audio_table.get(doc_id=expected_id)
        self.assertIsNotNone(audio_record)
        self.assertEqual(audio_record["text"], "Hello, world!")
        self.assertEqual(audio_record["language"], "en")
        self.assertEqual(audio_record["length"], 10)
        self.assertEqual(audio_record["transcribed_at"], "2024-01-01 12:00:00")

    def test_get_all_audio(self):
        audio_records = [
            {"text": "Hello, world!", "language": "en", "length": 10, "transcribed_at": "2024-01-01 12:00:00"},
            {"text": "Bonjour le monde!", "language": "fr", "length": 15, "transcribed_at": "2024-01-01 12:00:00"},
            {"text": "Hola, mundo!", "language": "es", "length": 12, "transcribed_at": "2024-01-01 12:00:00"}
        ]
        for audio_record in audio_records:
            self.audio_table.insert(audio_record)

        expected_result = audio_records
        actual_result = self.db.get_all_audio()
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(3, len(actual_result))

    def test_generate_key_for_user(self):
        user = "test_user"
        api_key_for_test_user = self.api_key_table.get(Query().user == user)
        self.assertIsNone(api_key_for_test_user, 'API key for test_user should not exist yet')

        api_key = self.db.generate_key_for_user(user)
        api_key_for_test_user = self.api_key_table.get(Query().user == user)
        self.assertIsNotNone(api_key_for_test_user, 'API key for test_user should exist now')
        self.assertEqual(api_key.key, api_key_for_test_user["key"])
        self.assertEqual(api_key.user, api_key_for_test_user["user"])

    def test_get_all_users(self):
        api_keys = self.db.get_all_api_keys()
        self.assertEqual(0, len(api_keys), 'No API keys should exist yet')
        users = ["user1", "user2", "user3"]
        for user in users:
            self.api_key_table.insert({"key": f"key-for-{user}", "user": user})
        
        api_keys = self.db.get_all_api_keys()
        self.assertEqual(3, len(api_keys))
    
    def test_truncate(self):
        audio_records = [
            {"text": "Hello, world!", "language": "en", "length": 10, "transcribed_at": "2024-01-01 12:00:00"},
            {"text": "Bonjour le monde!", "language": "fr", "length": 15, "transcribed_at": "2024-01-01 12:00:00"},
            {"text": "Hola, mundo!", "language": "es", "length": 12, "transcribed_at": "2024-01-01 12:00:00"}
        ]
        for audio_record in audio_records:
            self.audio_table.insert(audio_record)

        all_items = self.audio_table.all()
        self.assertEqual(3, len(all_items))
        self.db.truncate()
        all_items = self.db.get_all_audio()
        self.assertEqual(0, len(all_items))
        self.assertEqual([], all_items)

    def test_validate_api_key_valid_key(self):
        user = "test_user"
        api_key = self.db.generate_key_for_user(user)
        self.assertTrue(self.db.validate_api_key(api_key.key))

    def test_validate_api_key_invalid_key(self):
        self.assertFalse(self.db.validate_api_key("invalid_key"))
    
    def tearDown(self):
        self.db.db.close()
        os.remove(self.db_name)
