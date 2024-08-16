import unittest
from models.api_key import ApiKey

class ApiKeyTests(unittest.TestCase):
    def setUp(self):
        self.user = "test_user"

    def test_init(self):
        obj = ApiKey()
        self.assertIsNone(obj.key)
        self.assertIsNone(obj.user)
    
    def test_init_with_unpacked_values(self):
        dict = {"key": "test_key", "user": "test_user"}
        api_key = ApiKey(**dict)
        self.assertEqual(api_key.key, dict["key"])
        self.assertEqual(api_key.user, dict["user"])

    def test_generate(self):
        api_key = ApiKey.generate(self.user)
        self.assertIsInstance(api_key, ApiKey)
        self.assertIsNotNone(api_key.key)
        self.assertEqual(api_key.user, self.user)

    def test_generate_another_key_for_same_user(self):
        api_key_1 = ApiKey.generate(self.user)
        api_key_2 = ApiKey.generate(self.user)
        self.assertIsNotNone(api_key_1.key)
        self.assertIsNotNone(api_key_2.key)
        self.assertNotEqual(api_key_1.key, api_key_2.key)

    def test_to_dict(self):
        api_key = ApiKey.generate(self.user)
        api_key_dict = api_key.to_dict()
        self.assertEqual(2, len(api_key_dict.keys()))
        self.assertIn("key", api_key_dict)
        self.assertIn("user", api_key_dict)
