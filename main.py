import os
import uuid
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
    ordered_values = [values[el] if el in values.keys(
    ) else None for el in COLUMNS[table]]
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
    ordered_values = ", ".join(
        [f"`{key}`={val}" for key, val in values.items()])
    if arguments:
        q = f"UPDATE {table} SET {ordered_values} WHERE {arguments}"
        cursor.execute(q)
    else:
        cursor.execute(f"UPDATE {table} SET {ordered_values}")
    conn.commit()
    result = cursor.fetchall()
    return result


TABLES = ["user", "post", "postimages", "userlikedpost", "isfriend"]
COLUMNS = {table: get_columns(table) for table in TABLES}

#  r.post("http://localhost:8000/fetch-add-user", json={"username": "@redn1njaA", "email": "ostap.seryvko@ucu.edu.ua", "profilepicture": "None", "currmusic": "None", "password": "123"})


@app.post("/fetch-add-user")
async def fetch_add(request: Request, response: Response):
    item = await request.json()
    try:
        username = item["username"]
        password = item["password"]
        email = item["email"]
        token = str(
            int(hashlib.sha256((username.encode()+password.encode())).hexdigest(), 16))
        item["password"] = token
        user_exists = select_query("user", f"`username`= '{username}'")
        email_exists = select_query("user", f"`email` = '{email}'")
        if user_exists == [] and email_exists == []:
            insert_query("user", item)
    
            response.status_code = status.HTTP_200_OK
            return JSONResponse(content={"token": token})
        elif user_exists != []:
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
    userdata = select_query("user", f"`username`= '{username}'")
    if userdata == []:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
    else:
        userdata = userdata[0]
    avatar, song = userdata[2], userdata[3]
    posts = select_query("post", f"`username`= '{username}'")
    post_ids = {post[0]: dict(zip(COLUMNS["post"], post)) for post in posts}

    images = {post_id: select_query(
        "postimages", f"`idpost`={post_id}") for post_id in post_ids.keys()}
    images = {post_id: [image[2] for image in val]
              for post_id, val in images.items()}
    friends = select_query("isfriend", f"`username1`= '{username}'")

    # avatar_data = avatar
    try:
        with open("./data/" + avatar, "r") as file:
            avatar_data = file.read()
    except TypeError:
        # status.HTTP_400_BAD_REQUEST
        # return
        avatar_data = None
    data = {"username": username, "avatar": avatar_data, "song": song, "posts": {
        "data": post_ids, "images": images}, "friends": [friend[1] for friend in friends]}
    response.status_code = status.HTTP_200_OK
    return data


@app.post("/fetch-add-friend")
async def fetch_friend(request: Request, response: Response):
    item = await request.json()
    try:
        insert_query('isfriend', item)
    except sqlite3.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-remove-friend")
async def fetch_no_friend(request: Request, response: Response):
    item = await request.json()
    user1, user2 = item["username1"], item["username2"]
    delete_query(
        'isfriend', f"`username1` = '{user1}' AND `username2` = '{user2}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-modify-profile-photo")
async def fetch_profile_photo(request: Request, response: Response):
    # TODO
    # changes are needed here
    item = await request.json()
    filename = str(uuid.uuid4())
    while os.path.isfile("./data/" + filename):
        filename = str(uuid.uuid4())
    with open("./data/" + filename, "w") as file:
        file.write(item["image"])
    username = item["username"]
    update_query(
        "user", {"profilePicture": f"'{filename}'"}, f"`username`='{username}'")
    response.status_code = status.HTTP_200_OK

# @app.get("/fetch-photo/{image}")
# async def fetch_photo(image: Request, response: Response):
#     # TODO
#     # changes are needed here
#     # item = await request.json()
#     # filename = str(uuid.uuid4())
#     # while os.path.isfile("./data/" + filename):
#     #     filename = str(uuid.uuid4())
#     # with open("./data/" + filename, "w") as file:
#     #     file.write(item["image"])
#     # print("./data/" + filename)
#     # username = item["username"]
#     # update_query(
#     #     "user", {"profilePicture": f"'{filename}'"}, f"`username`='{username}'")

#     response.status_code = status.HTTP_200_OK


@app.post("/fetch-modify-music")
async def fetch_photo(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    username, song = items[0], items[1]
    update_query("user", f"`currmusic`='{song}'", f"`username`='{username}'")
    response.status_code = status.HTTP_200_OK


@app.post("/fetch-new-post")
async def fetch_new_post(request: Request, response: Response):
    # TODO
    # changes are needed here
    item = await request.json()
    username = item["username"]
    new_id = select_query("post")[-1][0]
    new_id += 1
    items = {"idpost": new_id, "username": username, "article": item["article"],  "added": datetime.now(
    ), "modified": datetime.now(), "nlikes": 0}
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
    try:
        username, post, author = item["username"], item["post"], item["author"]
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    hasliked = select_query(
        "userlikedpost", f"`idPost` = {post} and `userUsername`='{author}' ")
    print(hasliked)
    response.status_code = status.HTTP_200_OK
    if hasliked == []:
        res =JSONResponse(content={"liked": "0"})
    else:
        res = JSONResponse(content={"liked": "1"})
    return res


@app.post("/fetch-like")
async def fetch_like(request: Request, response: Response):
    item = await request.json()
    items = list(item.values())
    post_id, username, author = items[0], items[1], items[2]
    hasliked = select_query(
        "userlikedpost", f"`userUsername` = '{username}' and `idPost` = {post_id}")
    if hasliked == []:
        add = 1
    else:
        add = -1
    post = list(select_query(
        "post", f"`idpost` = {post_id} AND `username`= '{author}'"))
    # print(post)
    if post != []:
        post = list(post[0])
    else:
        res = JSONResponse(content={"liked": "0"})
        return res
    print(post)
    if add == 1:
        insert_query("userlikedpost", {
                     "userUsername": username, "idPost": post_id, "authorUsername": author})
        res = JSONResponse(
            content={"liked": "1", "nlikes": max(post[-1] + add, 0)})
    else:
        delete_query("userlikedpost",
                     f"`userUsername` = '{username}' and `idPost` = {post_id}")
        res = JSONResponse(
            content={"liked": "0", "nlikes": max(post[-1] + add, 0)})
    post[-1] = max(post[-1] + add, 0)
    update_query(
        "post", {'nlikes': post[-1]}, f"`idpost` = {post_id} AND `username`= '{username}'")
    response.status_code = status.HTTP_200_OK
    return res


@app.post("/fetch-main-page")
async def main(request: Request, response: Response):
    item = await request.json()
    username = item["username"]
    friends = [names[1] for names in select_query(
        "isfriend", f"`username1`= '{username}'")]
    posts = []
    friend_avatars = {}
    for friend in friends:
        data = await fetch_show_profile(friend, response)
        cur_posts = data["posts"]
        friend_avatars[friend] = data["avatar"]
        posts.append(cur_posts)
    posts_dates = [val["data"] for val in posts]
    posts_dates = [sorted(list(post.values()), key=lambda x: max(
        x["added"], x["modified"]), reverse=True) if post else None for post in posts_dates]
    posts_dates = [item for subitem in posts_dates for item in subitem]
    posts_dates = sorted(posts_dates, key=lambda x: max(
        x["added"], x["modified"]), reverse=True)
    response.status_code = status.HTTP_200_OK
    selected_posts = posts_dates[:max(len(posts_dates), 10)]
    selected_avatars = []
    for post in selected_posts:
        selected_avatars = {
            post["username"]: friend_avatars[post["username"]] for post in selected_posts}
    return {"posts": selected_posts, "avatars": selected_avatars}


@app.post("/fetch-login")
async def fetch_login(request: Request, response: Response):
    item = await request.json()
    username, password = item["username"], item["password"]
    try:
        login = select_query("user", f"`username`= '{username}'")[0]
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    if login[-1] == str(int(hashlib.sha256((username.encode()+password.encode())).hexdigest(), 16)):
        response.status_code = status.HTTP_200_OK
        return JSONResponse(
            content={"token": login[-1]}
        )
    else:
        response.status_code = status.HTTP_403_FORBIDDEN


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
