from flask import request, jsonify
from werkzeug.exceptions import Unauthorized
from db import DB

def authorize_request(function):
    """
    A decorator that authorizes a request based on the presence of an API key in the request headers.
    """
    AUTHORIZATION_HEADER = 'X-API-KEY'

    def inner(*args, **kwargs):
        if AUTHORIZATION_HEADER not in request.headers:
            raise Unauthorized("API key missing")
        
        api_key = request.headers[AUTHORIZATION_HEADER]
        if not DB().validate_api_key(api_key):
            raise Unauthorized("Invalid API key")
        
        return function(*args, **kwargs)
    
    return inner    
