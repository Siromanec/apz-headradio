from fastapi import Cookie, Response, status
import repository

def validate_token(username: str, token: str):
    active_token = repository.get_token(username)
    if token is None:
        return False
    return active_token == token

def unauthorized(username: str, response: Response, token: str):
    if not validate_token(username, token):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Unauthorized"}
    return None