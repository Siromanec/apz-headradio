import psycopg2
from query_func import select_query, insert_query, delete_query, update_query


conn = psycopg2.connect(database="likes_db",
                        host="localhost",
                        user="root",
                        password="root_pass",
                        port="5432")

cur = conn.cursor()


def get_user_has_liked_post(user: str, post: int) -> int:
    """Returns 1 if user has liked post, 0 if hasn't"""
    hasliked = 0 if select_query(cur, "likes", f"post_id = {post} and username = '{user}' ") == [] else 1
    return hasliked


def add_like(user: str, post: int):
    insert_query(cur, conn, "likes", {"post_id": post, "username": user})


def remove_like(user: str, post: int):
    delete_query(cur, conn, "likes", f"post_id = {post} and username = '{user}' ")


def get_likes(post: int) -> list:
    return select_query(cur, "likes", f"post_id = {post}")


if __name__ == "__main__":
    add_like("admin", 1)
    print(get_user_has_liked_post("admin", 1))
    print(get_likes(1))
    remove_like("admin", 1)
    print(get_likes(1))
