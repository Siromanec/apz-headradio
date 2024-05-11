import uvicorn
from controller import app

# some app setup (on start, on exit, etc)
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)