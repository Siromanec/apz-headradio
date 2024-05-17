from sqlalchemy import String, select, insert, delete, exists, Text, alias, table, join
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, aliased
import sqlalchemy
from sqlalchemy import exc


class Base(DeclarativeBase):
    ...


class Friends(Base):
    __tablename__ = "friends"
    username_follows: Mapped[str] = mapped_column(Text(), primary_key=True)
    username: Mapped[str] = mapped_column(Text(), primary_key=True)
    def __repr__(self) -> str:
        return f"Friend(username_follows={self.username_follows!r}, username={self.username!r})"


db_url = sqlalchemy.engine.URL.create(
    drivername="postgresql+psycopg2",
    database="friend_db",
    host="friend_db",  # TODO dynamic host
    username="root",
    password="root_pass",
    port="5432")

engine = sqlalchemy.engine.create_engine(db_url)
session: None | Session = None


def start_session():
    global session
    session = Session(engine)


def end_session():
    global session
    session.close()


def get_followers(username: str):
    return session.execute(select(Friends.username).where(Friends.username_follows == username)).all()


def get_following(username: str):
    return session.execute(select(Friends.username_follows).where(Friends.username == username)).all()


def get_friends(username: str):
    f1 = select(Friends).alias("f1")
    f2 = select(Friends).alias("f2")

    join_stmt = select(join(f1,f2, (f1.c.username == f2.c.username_follows) & (f2.c.username == f1.c.username_follows))).alias("join_stmt")
    final_stmt = select(join_stmt.c.username, join_stmt.c.username_follows).where(join_stmt.c.username == username)
    return session.execute(final_stmt).all()


# TODO: forward some error response
def add_friend(username_follows: str, username: str):
    friend = Friends(username_follows=username_follows, username=username)
    try:
        session.add(friend)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        import sys
        print(e, file=sys.stderr)


def remove_friend(username_follows: str, username: str):
    session.execute(
        delete(Friends).where(Friends.username_follows == username_follows).where(Friends.username == username))
    session.commit()


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
