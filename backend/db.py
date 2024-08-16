from tinydb import TinyDB, Query
from models.api_key import ApiKey


class DB:
    """
    A class representing a database.

    Attributes:
        db (TinyDB): The TinyDB instance representing the database.

    Methods:
        get(audio_id): Retrieve an audio record from the database based on its ID.
        insert_audio(audio): Insert an audio record into the database.
    """

    AUDIO_TABLE = 'Audio'
    API_KEY_TABLE = 'ApiKey'

    def __init__(self, db_name='db.json'):
        """
        Initialize the DB class.

        Creates a TinyDB instance and sets it as the database.
        """
        self.db = TinyDB(db_name)

    def get(self, audio_id):
        """
        Retrieve an audio record from the database based on its ID.

        Args:
            audio_id (int): The ID of the audio record to retrieve.

        Returns:
            dict: The audio record matching the given ID.
        """
        Audio = Query()
        return self.db.get(Audio.id == audio_id)

    def insert_audio(self, audio):
        """
        Insert an audio record into the database table "Audio".

        Args:
            audio (Audio): The audio record to insert.

        Returns:
            int: The ID of the inserted audio record.
        """
        audio_table = self.db.table(self.AUDIO_TABLE)
        return audio_table.insert(audio.to_dict())
    
    def get_all_audio(self):
        """
        Retrieve all audio records from the database.

        Returns:
            list: A list of all audio records in the database.
        """
        return self.db.table(self.AUDIO_TABLE).all()
    
    def generate_key_for_user(self, user):
        """
        Generate an API key for the given user and store it in the database.

        Args:
            user (str): The user for whom the API key is generated.

        Returns:
            str: The generated API key.
        """
        api_key = ApiKey.generate(user)
        api_key_table = self.db.table(self.API_KEY_TABLE)
        api_key_table.insert(api_key.to_dict())
        return api_key
    
    def truncate(self):
        """
        Remove all audio records from the database.
        """
        self.db.drop_table(self.AUDIO_TABLE)
