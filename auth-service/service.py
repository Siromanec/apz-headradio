# logic
import repository
import hashlib
import uuid

async def login(user, password):
    hashed_password = hashlib.sha256((user + password).encode("utf-8")).hexdigest()
    if await repository.login(user, hashed_password):
        return str(uuid.uuid4())

async def register(user, password, email):
    hashed_password = hashlib.sha256((user + password).encode("utf-8")).hexdigest()
    if await repository.register(user, hashed_password, email):
        return str(uuid.uuid4())
