from faker import Faker
from sqlalchemy import create_engine, text

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
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE posts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE messages (
                id SERIAL PRIMARY KEY,
                user_sender INTEGER REFERENCES users(id),
                user_receiver INTEGER REFERENCES users(id),
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );


        """))

        conn.commit()

    
def populate_db(datastore: Datastore):    
    with datastore.connection as conn:
        fake = Faker(['ja_JP']) 

        conn.execute(
            text("INSERT INTO users (username, name) VALUES (:username, :name);"),
            [{ 'username': fake.name(), 'name': fake.user_name() } for _ in range(100)]
        )
        conn.commit()


def post(datastore: Datastore, title: str, user_id: int, content: str): 
    with datastore.connection as conn:
        conn.execute(
            text("INSERT INTO posts (title, user_id, content) VALUES (:title, :user_id, :content);"),
            [{ 'title': title, 'user_id': user_id, 'content': content }]
        )
        conn.commit()


def timeline(datastore: Datastore):    
    with datastore.connection as conn:
        return conn.execute(
            text("SELECT p.title, u.username, p.content, p.created_at FROM posts p INNER JOIN users u on p.user_id = u.id LIMIT 100;")
        ).all()

    
# as an example of an inefficient query
def user_detail_summary(datastore: Datastore, username: str):
    with datastore.connection as conn:
        return conn.execute(
            text("SELECT u.username, u.name, u.created_at, (SELECT COUNT(p.id) FROM posts p WHERE p.user_id = u.id) as post_count, (SELECT COUNT(m.id) FROM messages m WHERE m.user_sender = u.id) as message_count FROM users u WHERE u.username = :username;"),
            { 'username': username }
        ).all()[0]

def user_posts(datastore: Datastore, username: str):
    with datastore.connection as conn:
        return conn.execute(
            text("SELECT p.title, p.content, p.created_at FROM posts p INNER JOIN users u on p.user_id = u.id WHERE u.username = :username;"),
            { 'username': username }
        ).all()