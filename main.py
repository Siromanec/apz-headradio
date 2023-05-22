from fastapi import FastAPI, Request, Response, status
import uvicorn
import sqlite3
from datetime import datetime
import hashlib
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
conn = sqlite3.connect("./database.db")
cursor = conn.cursor()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def main():
    return {"message": "Hello World"}

def get_columns(table):
    cursor.execute(f"pragma table_info('{table}')")
    result = cursor.fetchall()
    result = ([elem[1] for elem in result])
    return result

def cols_to_string(cols):
    return "'" + "', '".join([elem for elem in cols])+"'"
def select_query(table, arguments=None):
    if arguments:
        cursor.execute(f"SELECT * FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    return result


def insert_query(table, values):
    datacount = ("?, "*len(COLUMNS[table])).strip(", ")
    q = f"INSERT INTO {table} ({cols_to_string(COLUMNS[table])}) VALUES ({datacount})"
    ordered_values = [values[el] if el in values.keys() else None for el in COLUMNS[table]]
    cursor.execute(q, ordered_values)
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


def update_query(table, values, arguments=None):
    ordered_values = ", ".join([f"`{key}`={val}" for key, val in values.items()])
    print(ordered_values)
    if arguments:
        q = f"UPDATE {table} SET {ordered_values} WHERE {arguments}"
        print(q)
        cursor.execute(q)
    else:
        cursor.execute(f"UPDATE {table} SET {ordered_values}")
    conn.commit()
    result = cursor.fetchall()
    return result


TABLES = ["user", "post", "postimages", "userlikedpost", "isfriend"]
COLUMNS = {table: get_columns(table) for table in TABLES}
print(COLUMNS)

#  r.post("http://localhost:8000/fetch-add-user", json={"username": "@redn1njaA", "email": "ostap.seryvko@ucu.edu.ua", "profilepicture": "None", "currmusic": "None", "password": "123"})
@app.post("/fetch-add-user")
async def fetch_add(request: Request, response: Response):
    item = await request.json()
    try:
        username = item["username"]
        password = item["password"]
        email = item["email"]
        token = str(int(hashlib.sha256((username.encode()+password.encode())).hexdigest(), 16))
        item["password"] = token
        user_exists = select_query("user", f"`username`= '{username}'") 
        email_exists = select_query("user", f"`email` = '{email}'")
        
        if user_exists == [] and email_exists == []:
            insert_query("user", item)
            print(token)
            response.status_code = status.HTTP_200_OK
            return JSONResponse(content={"token": token})
        elif user_exists!= []:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return JSONResponse(content={"token": "400"})
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return JSONResponse(content={"token": "403"})
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content={"token": "500"})


@app.get("/fetch-show-user/{username}")
async def fetch_show_profile(username: str, response: Response):
    print(username)
    # item = await request.json()
    print(username)
    user_data = select_query("user", f"`username`= '{username}'")
    
    posts = select_query("post", f"`username`= '{username}'")
    print(posts)
    post_ids = {post[0]: dict(zip(COLUMNS["post"], post)) for post in posts}

    images = {post_id: select_query(
        "postimages", f"`idpost`={post_id}") for post_id in post_ids.keys()}
    images = {post_id: [image[2] for image in val]
              for post_id, val in images.items()}
    friends = select_query("isfriend", f"`username1`= '{username}'")


    data = {"username": username, "posts": {
        "data": post_ids, "images": images}, "friends": [friend[1] for friend in friends]}
    response.status_code = status.HTTP_200_OK
    return data


@app.post("/fetch-add-friend")
async def fetch_friend(request: Request, response: Response):
    item = await request.json()
    insert_query('isfriend', item)
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-remove-friend")
async def fetch_no_friend(request: Request, response: Response):
    item = await request.json()
    user1, user2 = list(item.values())
    delete_query(
        'isfriend', f"`username1` = '{user1}' AND `username2` = '{user2}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-modify-profile-photo")
async def fetch_photo(request: Request, response: Response):
    item = await request.json()
    # items = list(item.values())
    print(item)
    username, picturelink = item["username"], item[1]
    update_query(
        "user", f"`profilePicture`='{picturelink}'", f"`username`='{username}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-modify-music")
async def fetch_photo(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    username, song = items[0], items[1]
    update_query("user", f"`currmusic`='{song}'", f"`username`='{username}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-new-post")
async def fetch_new_post(request: Request, response: Response):
    item = await request.json()
    username = item["username"]
    new_id = select_query("post")[-1][0]
    new_id += 1
    items = {"idpost":new_id, "username": username, "article" : item["article"],  "added":datetime.now(), "modified":datetime.now(), "nlikes":0}
    insert_query("post", items)
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-edit-post")
async def fetch_edit_post(request: Request, response: Response):
    item = await request.json()
    idpost, username, text = list(item.values())
    update_query("post", f"`article`='{text}', `modified` = '{datetime.now()}'",
                 f"`idpost` = {idpost} AND `username`= '{username}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-delete-post")
async def fetch_delete_post(request: Request, response: Response):
    item = await request.json()
    idpost, username = list(item.values())
    delete_query("post", f"`idpost`={idpost} AND `username` = '{username}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-has-liked")
async def fetch_has_liked(request: Request, response: Response):
    item = await request.json()
    username, post = item["username"], item["post"]
    hasliked = select_query("userlikedpost", f"`userUsername` = '{username}' and `idPost` = {post}")
    response.status_code = status.HTTP_200_OK
    if hasliked == []:
        return JSONResponse(content={"liked": "0"})
    else:
        return JSONResponse(content={"liked": "1"})
        

@app.post("/fetch-like")
async def fetch_like(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    print(items)
    post_id, username= items[0], items[1]
    hasliked = select_query("userlikedpost", f"`userUsername` = '{username}' and `idPost` = {post_id}")
    if hasliked == []:
        add = 1
    else:
        add = -1
    post = list(select_query(
        "post", f"`idpost` = {post_id} AND `username`= '{username}'")[0])
    print(post)
    if add == 1:
        insert_query("userlikedpost", {"userUsername": username, "idPost": post_id, "authorUsername": post[1]})
        res = JSONResponse(content={"liked": "1", "nlikes": max(post[-1] + add, 0)})
    else:
        delete_query("userlikedpost", f"`userUsername` = '{username}' and `idPost` = {post_id}")
        res = JSONResponse(content={"liked": "0", "nlikes": max(post[-1] + add, 0)})
    print(post)
    post[-1] = max(post[-1] + add, 0)
    update_query(
        "post", {'nlikes':post[-1]}, f"`idpost` = {post_id} AND `username`= '{username}'")
    response.status_code = status.HTTP_200_OK
    return res

@app.get("/fetch-main-page")
async def main(request: Request, response: Response):
    item = await request.json()
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-login")
async def fetch_login(request: Request, response: Response):
    item = await request.json()
    # items = list(item.values())
    print(item)
    username, password = item["username"], item["password"]
    try:
        login = select_query("user", f"`username`= '{username}'")[0]
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    if login[-1] == str(int(hashlib.sha256((username.encode()+password.encode())).hexdigest(), 16)):
        response.status_code = status.HTTP_200_OK
        return  JSONResponse(
            content={"token": login[-1]}
        )
    else:
        response.status_code = status.HTTP_403_FORBIDDEN


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
