from sqlalchemy import String, select, insert, delete, exists, update, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import sqlalchemy
from sqlalchemy import exc

class Base(DeclarativeBase):
    ...

class Profile(Base):
    __tablename__ = "profile_user_data"

    username: Mapped[str] = mapped_column(Text(), primary_key=True)
    profile_picture: Mapped[str] = mapped_column(String(256))
    selected_music: Mapped[str] = mapped_column(String(256))
    motto: Mapped[str] = mapped_column(String(256))

    def __repr__(self) -> str:
        return f"Profile(username={self.username!r}, profile_picture={self.profile_picture!r}, selected_music={self.selected_music!r}, motto={self.motto!r})"
    
db_url = sqlalchemy.engine.URL.create(
    drivername="postgresql+psycopg2",
    database="profile_db",
    host="localhost", # TODO dynamic host
    username="root",
    password="root_pass",
    port="5433")

engine = sqlalchemy.engine.create_engine(db_url)
session: None | Session = None

def start_session():
    global session
    session = Session(engine)

def end_session():
    global session
    session.close()

def get_pfp(user: str) -> str:
    profile = [*session.execute(select(Profile).where(Profile.username == user))][0][0]
    return profile.profile_picture

def get_user_data(user: str) -> str:
    profile = [*session.execute(select(Profile).where(Profile.username == user))][0][0]
    return profile

def modify_profile_photo(user: str, user_data: dict):
    session.execute(update(Profile).where(Profile.username == user).values(profile_picture=user_data['profilePicture']))
    session.commit()

def set_music(user: str, song_name: str):
    session.execute(update(Profile).where(Profile.username == user).values(selected_music=song_name))
    session.commit()

def create_profile(user: str):
    profile = Profile(username=user, profile_picture="", selected_music="", motto="")
    try:
        session.add(profile)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        import sys
        print(e, file=sys.stderr)

def __test_repo():
    start_session()
    create_profile("username")
    print(get_user_data("username"))
    modify_profile_photo("username", {"profilePicture": "test", "username": "test"})
    print(get_user_data("username"))
    set_music("username", "test")
    print(get_user_data("username"))
    end_session()

if __name__ == "__main__":
    __test_repo()
