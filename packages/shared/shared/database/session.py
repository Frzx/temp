from sqlalchemy import Engine, create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import sessionmaker

def create_engine(database_url: str, *, echo: bool = False) -> Engine:
    return sqlalchemy_create_engine(database_url, echo=echo)

def create_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False)