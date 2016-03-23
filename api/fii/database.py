from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fii.settings import Config

def get_store():
    uri = '{}://{}:{}@{}/{}'.format(Config.RDBMS, Config.DB_USER,
                                    Config.DB_PASS, Config.DB_HOST,
                                    Config.DB_NAME)
    engine = create_engine(uri)
    Store = sessionmaker(bind=engine)
    store = Store()
    return store
