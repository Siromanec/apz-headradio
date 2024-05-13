from sqlalchemy import String, select, insert, delete, exists, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import sqlalchemy
from sqlalchemy import exc


class Base(DeclarativeBase):
    ...

class Auth(Base):
    __tablename__ = "auth"

    username: Mapped[str] = mapped_column(Text(), primary_key=True)
    email: Mapped[str] = mapped_column(Text())
    passwordhash: Mapped[str] = mapped_column(Text())

    def __repr__(self) -> str:
        return f"Auth(username={self.username!r}, email={self.email!r}, passwordhash={self.passwordhash!r})"
    
db_url = sqlalchemy.engine.URL.create(
    drivername="postgresql+psycopg2",
    database="auth_db",
    host="auth_db", # TODO dynamic host
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

def login(user: str, password: str):
    return [*session.execute(select(select(Auth).where(Auth.username == user).where(Auth.passwordhash == password).exists()))][0][0]

def register(user: str, password: str, email:str):
    auth = Auth(username=user, passwordhash=password, email=email)
    try:
        session.add(auth)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        import sys
        print(e, file=sys.stderr)

def __test_repo():
    start_session()
    register("user", "1234", "1234@gmail.com")
    print(login("user", "1234"))
    end_session()

if __name__ == "__main__":
    __test_repo()