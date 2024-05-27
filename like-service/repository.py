from typing import Tuple, Sequence, Any

from sqlalchemy import String, select, insert, delete, exists, Text, Row
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import sqlalchemy
from sqlalchemy import exc
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class Base(DeclarativeBase):
    ...


class Likes(Base):
    __tablename__ = "likes"

    username: Mapped[str] = mapped_column(Text(), primary_key=True)
    post_id: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Like(username={self.username!r}, post={self.post_id!r})"


db_url = sqlalchemy.engine.URL.create(
    drivername="postgresql+asyncpg",
    database="likes_db",
    host="likes_db", # TODO dynamic host
    username="root",
    password="root_pass",
    port="5432")

engine = create_async_engine(db_url)
session: None | AsyncSession = None


async def start_session():
    global session
    async with engine.begin() as conn:
        session = AsyncSession(conn)


async def end_session():
    global session
    await session.close()
    await engine.dispose()


async def has_liked(user: str, post: int) -> int:
    async with engine.connect() as conn:
        hasliked = [*await conn.execute(select(select(Likes).where(Likes.post_id == post).where(Likes.username == user).exists()))][0][0]
        return hasliked


# TODO: forward some error response
async def add_like(user: str, post: str):
    async with engine.connect() as conn:
        try:
            print("Adding like", user, post)
            await conn.execute(insert(Likes).values(username=user, post_id=int(post)))
            await conn.commit()
        except exc.IntegrityError as e:
            print(e, file=sys.stderr)


async def remove_like(user: str, post: str):
    async with engine.connect() as conn:
        await conn.execute(delete(Likes).where(Likes.post_id == int(post)).where(Likes.username == user))
        await conn.commit()


async def get_likes(post: str) -> Sequence[Row[tuple[Any, ...] | Any]]:
    print(post)
    async with engine.connect() as conn:
        result = await conn.execute(select(Likes).where(Likes.post_id == post))
        return result.fetchall()


def __test_db():
    print("-" * 20 + " test_db " + "-" * 20)
    global session
    session = Session(engine)
    like1 = Likes(username="admin", post_id=1)
    like2 = Likes(username="admin", post_id=2)
    session.add_all([like1, like2])
    session.commit()
    for like in session.execute(select(Likes)):
        print(like)
        ...

    for like in session.execute(select(Likes).where(Likes.post_id == 1).where(Likes.username == "admin")):
        print(like)
        ...
    for like in session.execute(
            select(select(Likes).where(Likes.post_id == 1).where(Likes.username == "admin").exists())):
        print(like)
        ...

    print()
    for like in session.execute(select(Likes).where(Likes.post_id == 1)):
        print(like)
        ...

    session.execute(delete(Likes).where(Likes.post_id == 1).where(Likes.username == "admin"))
    session.commit()
    for like in session.execute(select(Likes).where(Likes.post_id == 1).where(Likes.username == "admin")):
        print(like)
        ...
    session.execute(delete(Likes))
    session.commit()
    session.close()


def __test_repo():
    print("-" * 20 + " test_repo " + "-" * 20)
    start_session()
    print(get_likes(1))
    add_like("admin", 1)
    add_like("user", 1)
    add_like("admin", 2)
    add_like("admin", 2)
    print(has_liked("admin", 1))
    print(has_liked("admin", 3))
    print(get_likes(1))

    remove_like("admin", 1)
    remove_like("user", 1)
    remove_like("admin", 2)
    remove_like("admin", 42)
    end_session()


if __name__ == "__main__":
    # __test_db()
    __test_repo()
