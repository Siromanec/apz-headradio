# logic
import repository
import hashlib
import uuid

def login(user, password):
    hashed_password = hashlib.sha256((user + password).encode("utf-8")).hexdigest()
    if repository.login(user, hashed_password):
        return str(uuid.uuid4())
    return "No such user"

def register(user, password, email):
    hashed_password = hashlib.sha256((user + password).encode("utf-8")).hexdigest()
    repository.register(user, hashed_password, email)
