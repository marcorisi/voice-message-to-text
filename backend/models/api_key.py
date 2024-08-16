import secrets

class ApiKey:
    """
    Represents an api key object and provides methods for key generation.
    """

    @classmethod
    def generate(cls, user):
        """
        Generates a new api key for the user.

        Parameters:
        - user (str): The user for whom the api key is generated.
        """
        api_key = cls()
        api_key.key = secrets.token_urlsafe(32)
        api_key.user = user
        return api_key

    def __init__(self):
        """
        Initializes an Api Key object.
        """
        self.key = None
        self.user = None
    
    def to_dict(self):
        """
        Converts the Api Key object to a dictionary that can be stored in the database.
        The returned dictionary contains only a few relevant properties.

        Returns:
        - dict: A dictionary representation of the Api Key object.
        """
        PROPERTY_TO_KEEP = ["key", "user"]
        dict = self.__dict__
        return {key: dict[key] for key in PROPERTY_TO_KEEP}
