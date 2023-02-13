from faker import Faker
from sqlalchemy import create_engine, text, select

class Datastore:
    def __init__(self, username, password, hostname, dbname):
        self.engine = create_engine(
            f"postgresql+psycopg://{username}:{password}@{hostname}/{dbname}",
            echo=True, 
            future=True
        )

    @property
    def connection(self):
        return self.engine.connect()


def init(datastore: Datastore):
    with datastore.connection as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS posts (
                id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
                ,title       TEXT
                ,username    TEXT 
                ,content     TEXT
                ,created_at  TIMESTAMP NOT NULL DEFAULT clock_timestamp()::timestamp
            );
        """))

        conn.commit()

    
def populate_db(datastore: Datastore):    
    with datastore.connection as conn:
        fake = Faker(['ja_JP']) 
        conn.execute(
            text("INSERT INTO posts (title, username, content) VALUES (:title, :username, :content);"),
            [{ 'title': fake.sentence(), 'username': fake.name(), 'content': fake.text()} for _ in range(100)]
        )
        conn.commit()


def get_timeline(datastore: Datastore):    
    with datastore.connection as conn:
        return conn.execute(
            text("SELECT title, username, content, created_at FROM posts LIMIT 100;")
        ).all()