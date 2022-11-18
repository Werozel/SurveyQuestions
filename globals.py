from pymorphy2 import MorphAnalyzer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config
import nltk

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@"
                       f"{config.db_host}:{config.db_port}/{config.db_name}")
session_factory = sessionmaker(bind=engine)
session = session_factory()
Base = declarative_base()

morph = MorphAnalyzer()


def create_tables():
    # Necessary imports for db to register
    from models.Question import Question
    Base.metadata.create_all(engine)


def init():
    create_tables()

    nltk.download("punkt")
    nltk.download("stopwords")
