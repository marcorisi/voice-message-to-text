from tinydb import TinyDB, Query


class DB:
    """
    A class representing a database.

    Attributes:
        db (TinyDB): The TinyDB instance representing the database.

    Methods:
        get(audio_id): Retrieve an audio record from the database based on its ID.
        insert_audio(audio): Insert an audio record into the database.
    """

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
        Insert an audio record into the database.

        Args:
            audio (Audio): The audio record to insert.

        Returns:
            int: The ID of the inserted audio record.
        """
        return self.db.insert(audio.to_dict())
    
    def get_all(self):
        """
        Retrieve all audio records from the database.

        Returns:
            list: A list of all audio records in the database.
        """
        return self.db.all()
