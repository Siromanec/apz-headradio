from contextlib import asynccontextmanager

import uvicorn
from controller import app
import repository


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8079)