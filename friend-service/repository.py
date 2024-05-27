from sqlalchemy import String, select, insert, delete, exists, Text, alias, table, join
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, aliased
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Base(DeclarativeBase):
    ...


class Friends(Base):
    __tablename__ = "friends"
    username_follows: Mapped[str] = mapped_column(Text(), primary_key=True)
    username: Mapped[str] = mapped_column(Text(), primary_key=True)
    def __repr__(self) -> str:
        return f"Friend(username_follows={self.username_follows!r}, username={self.username!r})"


db_url = sqlalchemy.engine.URL.create(
    drivername="postgresql+asyncpg",
    database="friend_db",
    host="friend_db",  # TODO dynamic host
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


async def get_followers(username: str):
    async with engine.connect() as conn:
        followers = await conn.execute(select(Friends.username).where(Friends.username_follows == username))
        return followers.all()


async def get_following(username: str):
    async with engine.connect() as conn:
        following = await conn.execute(select(Friends.username_follows).where(Friends.username == username))
        return following.all()


async def get_friends(username: str):
    async with engine.connect() as conn:
        f1 = alias(Friends)
        f2 = alias(Friends)
        join_stmt = select(join(f1, f2, (f1.c.username == f2.c.username_follows) & (f2.c.username == f1.c.username_follows))).alias("join_stmt")
        final_stmt = select(join_stmt.c.username, join_stmt.c.username_follows).where(join_stmt.c.username == username)
        return await conn.execute(final_stmt)


# TODO: forward some error response
async def add_friend(username_follows: str, username: str):
    async with engine.connect() as conn:
        try:
            await conn.execute(insert(Friends).values(username_follows=username_follows, username=username))
            await conn.commit()
        except exc.IntegrityError as e:
            import sys
            print(e, file=sys.stderr)


async def remove_friend(username_follows: str, username: str):
    async with engine.connect() as conn:
        await conn.execute(delete(Friends).where(Friends.username_follows == username_follows).where(Friends.username == username))
        await conn.commit()


def __test_repo():
    print("-" * 20 + " test_repo " + "-" * 20)
    start_session()
    add_friend("fan", "admin")
    add_friend("fan", "username")
    add_friend("admin", "username")
    print(get_friends("fan"))
    print(get_friends("admin"))
    print(get_friends("username"))

    remove_friend("fan", "username")
    print(get_friends("username"))

    end_session()


if __name__ == "__main__":
    __test_repo()
