from sqlalchemy import String, select, insert, delete, exists, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
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
    database="friendzone_db",
    host="friendzone_db", # TODO dynamic host
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


def get_friends(username: str):
    return [*session.execute(select(Friends).where(Friends.username == username))]


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
    session.execute(delete(Friends).where(Friends.username_follows == username_follows).where(Friends.username == username))
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