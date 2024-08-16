from flask import request, jsonify

def authorize_request(function):
    """
    A decorator that authorizes a request based on the presence of an API key in the request headers.
    """
    AUTHORIZATION_HEADER = 'X-API-KEY'

    def error_response(message: str = None):
        message = message or "Unauthorized"
        response = jsonify({ "error" : message })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 401
    
    def inner(*args, **kwargs):
        if AUTHORIZATION_HEADER not in request.headers:
            return error_response()
        
        return function(*args, **kwargs)
    
    return inner    
