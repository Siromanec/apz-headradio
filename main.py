from fastapi import FastAPI, Request, Response, status
import uvicorn
import sqlite3
from datetime import datetime
import hashlib

app = FastAPI()
conn = sqlite3.connect("./database.db")
cursor = conn.cursor()


def get_columns(table):
    cursor.execute(f"pragma table_info('{table}')")
    result = cursor.fetchall()
    result = "'" + "', '".join([elem[1] for elem in result])+"'"
    return result


def select_query(table, arguments=None):
    if arguments:
        cursor.execute(f"SELECT * FROM {table} WHERE {arguments}")
    else:
        cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    return result


def insert_query(table, values):
    datacount = ("?, "*len(COLUMNS[table].split("', '"))).strip(", ")
    q = f"INSERT INTO {table} ({COLUMNS[table]})VALUES ({datacount})"
    cursor.execute(q, values)
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
    if arguments:
        q = f"UPDATE {table} SET {values} WHERE {arguments}"
        print(q)
        cursor.execute(q)
    else:
        cursor.execute(f"UPDATE {table} SET {values}")
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
    items = list(item.values())
    username = items[0]
    password = items[-1]
    token = str(int(hashlib.sha256((username.encode()+password.encode())).hexdigest(), 16))
    items[-1] = token
    is_in_db = select_query("user", f"`username`= '{username}'")
    if is_in_db == []:
        insert_query("user", items)
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST


@app.get("/fetch-show-user")
async def fetch_show_profile(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    username = items[0]
    user_data = select_query("user", f"`username`= '{username}'")
    posts = select_query("post", f"`username`= '{username}'")
    post_ids = {post[0]: post[2:] for post in posts}
    images = {post_id: select_query(
        "postimages", f"`idpost`={post_id}") for post_id in post_ids.keys()}
    images = {post_id: [image[2] for image in val]
              for post_id, val in images.items()}
    friends = select_query("isfriend", f"`username1`= '{username}'")
    data = {"user": user_data[0][0], "posts": {
        "messages": post_ids, "images": images}, "friends": [friend[1] for friend in friends]}
    response.status_code = status.HTTP_200_OK
    return data


@app.post("/fetch-add-friend")
async def fetch_friend(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    insert_query('isfriend', items)
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
    items = list(item.values())
    username, picturelink = items[0], items[1]
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
    items = list(item.values)
    username = items[1]
    try:
        new_id = select_query("post", f"`username`='{username}'")[-1][-1]
    except:
        new_id = 1
    new_id += 1
    items = [new_id] + items + [datetime.now(), datetime.now(), 0]
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


@app.post("/fetch-like")
async def fetch_like(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    post_id, username, add = items[0], items[1], items[2]
    post = list(select_query(
        "post", f"`idpost` = {post_id} AND `username`= '{username}'")[0])
    print(post)
    post[-1] = max(post[-1] + add, 0)
    update_query(
        "post", f"`nlikes`={post[-1]}", f"`idpost` = {post_id} AND `username`= '{username}'")
    response.status_code = status.HTTP_200_OK


@app.get("/fetch-main-page")
async def main(request: Request, response: Response):
    item = await request.json()
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-login")
async def fetch_login(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    username, password = items[0], items[-1]
    try:
        login = select_query("user", f"`username`= '{username}'")[0]
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    if login[-1] == str(int(hashlib.sha256(username.encode()+password.encode())).hexdigest(), 16):
        response.status_code = status.HTTP_200_OK
        return {"token": login[-1]}
    else:
        response.status_code = status.HTTP_403_FORBIDDEN


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)