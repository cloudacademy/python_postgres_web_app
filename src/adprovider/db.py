from random import randint

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


def delay(datastore: Datastore, time: int=None): 
    if not time:
        time = randint(1, 3)

    with datastore.connection as conn:
        conn.execute(text("pg_sleep(:time);"), [{ 'time': time }])
        conn.commit()
