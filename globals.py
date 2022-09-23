from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@"
                       f"{config.db_host}:{config.db_port}/{config.db_name}")
session_factory = sessionmaker(bind=engine)
session = session_factory()
Base = declarative_base()


def create_tables():
    # Necessary imports
    from models.Question import Question
    Base.metadata.create_all(engine)
