from fastapi import FastAPI, Request
import uvicorn
import sqlite3

app = FastAPI()
conn = sqlite3.connect("./database.db")
cursor = conn.cursor()

def get_columns(table):
    cursor.execute(f"DESCRIBE {table}")
    result = cursor.fetchall()
    return "`" +"`, `".join([entry[0] for entry in result])+"`"
    
def select_query(table, arguments=None):
    if arguments:
        cursor.execute(f"SELECT * FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()

    return "<br>".join([",".join([str(el) for el in row]) for row in result])
    
        
def insert_query(table, values):
    cursor.execute(f"INSERT INTO {table} ({COLUMNS[table]})VALUES ({values})")
    conn.commit()
    result = cursor.fetchall()
    return result

def delete_query(table, arguments=None):
    if arguments:
        cursor.execute(f"DELETE FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    result = cursor.fetchall()
    return result

def update_query(table, values, arguments):
    if arguments:
        cursor.execute(f"UPDATE {table} SET {values} WHERE {arguments}")
    else:
        cursor.execute(f"UPDATE {table} SET {values}")
    conn.commit()
    result = cursor.fetchall()
    return result

TABLES = ["user", "post", "postimages", "userlikedpost", "isfriend"]
COLUMNS = {table:get_columns(table) for table in TABLES}

@app.post("/fetch-add-user")
async def fetch_add(request: Request):
    item = await request.json()

@app.get("/fetch-show-user")
async def fetch_show_profile(request: Request):
    item = await request.json()

@app.post("/fetch-add-friend")
async def fetch_friend(request: Request):
    item = await request.json()

@app.post("/fetch-remove-friend")
async def fetch_no_friend(request: Request):
    item = await request.json()

@app.get("/fetch-show-friends")
async def fetch_show_friends(request: Request):
    item = await request.json()

@app.post("/fetch-modify-profile-photo")
async def fetch_photo(request: Request):
    item = await request.json()

@app.post("/fetch-modify-music")
async def fetch_photo(request: Request):
    item = await request.json()

@app.post("/fetch-new-post")
async def fetch_new_post(request: Request):
    item = await request.json()

@app.post("/fetch-edit-post")
async def fetch_edit_post(request: Request):
    item = await request.json()

@app.get("/fetch-show-posts")
async def fetch_show_posts(request: Request):
    item = await request.json()

@app.post("/fetch-like")
async def fetch_like(request:Request):
    item = await request.json()

@app.get("/fetch-show-likes")
async def fetch_show_likes(request:Request):
    item = await request.json()





if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    

