from pymorphy2 import MorphAnalyzer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_bootstrap import Bootstrap

import config
import nltk

engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@"
                       f"{config.db_host}:{config.db_port}/{config.db_name}")
session_factory = sessionmaker(bind=engine)
session = session_factory()
Base = declarative_base()

morph = MorphAnalyzer()


def get_app() -> Flask:
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.jinja_env.globals.update(REQUEST_1="Вы считаете себя недооцененным?")
    app.jinja_env.globals.update(REQUEST_2="REQUEST_2")
    app.jinja_env.globals.update(REQUEST_3="REQUEST_3")

    return app


app = get_app()


def create_tables():
    # Necessary imports for db to register
    from models.Question import Question
    Base.metadata.create_all(engine)


def init():
    create_tables()

    nltk.download("punkt")
    nltk.download("stopwords")
