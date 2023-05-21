from fastapi import FastAPI, Request
import uvicorn
import sqlite3

app = FastAPI()
conn = sqlite3.connect("./database.db")
cur = conn.cursor()
cur.execute("SELECT * FROM test")








if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    

