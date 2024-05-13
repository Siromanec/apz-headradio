# logic
import repository
import _sha256
import uuid

def login(user, password):
    if repository.login(user, password):
        return str(uuid.uuid4())

def register(user, password, email):
    hashed_password = _sha256.sha256(user + password).hexdigest()
    repository.register(user, hashed_password, email)
