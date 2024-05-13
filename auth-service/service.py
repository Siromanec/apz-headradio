# logic
import repository
import hashlib
import uuid

def login(user, password):
    if repository.login(user, password):
        return str(uuid.uuid4())

def register(user, password, email):
    hashed_password = hashlib.sha256(user + password).hexdigest()
    repository.register(user, hashed_password, email)
