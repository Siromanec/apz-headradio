from fastapi import FastAPI, Request
import uvicorn
import sqlite3

app = FastAPI()
conn = sqlite3.connect("./database.db")
cur = conn.cursor()

@app.post("/fetch-add-user")
async def fetch_add(request: Request):
    pass

@app.get("/fetch-show-user")
async def fetch_show_profile(request: Request):
    pass

@app.post("/fetch-add-friend")
async def fetch_friend(request: Request):
    pass

@app.post("/fetch-remove-friend")
async def fetch_no_friend(request: Request):
    pass

@app.get("/fetch-show-friends")
async def fetch_show_friends(request: Request):
    pass

@app.post("/fetch-modify-profile-photo")
async def fetch_photo(request: Request):
    pass

@app.post("/fetch-modify-music")
async def fetch_photo(request: Request):
    pass

@app.post("/fetch-new-post")
async def fetch_new_post(request: Request):
    pass

@app.post("/fetch-edit-post")
async def fetch_edit_post(request: Request):
    pass

@app.get("/fetch-show-posts")
async def fetch_show_posts(request: Request):
    pass

@app.post("/fetch-like")
async def fetch_like(request:Request):
    pass

@app.get("/fetch-show-likes")
async def fetch_show_likes(request:Request):
    pass





if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    

