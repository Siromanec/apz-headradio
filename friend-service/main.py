import uvicorn
from controller import app

# some app setup (on start, on exit, etc)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)