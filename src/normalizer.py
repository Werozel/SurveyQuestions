from sqlalchemy.orm import Session
from pymorphy2 import MorphAnalyzer
from models.Question import Question
import re
import nltk


def __split_str(s: str) -> list[str]:
    return re.split("[,.\-;!?_: ()»«/]", s)


def __has_alpha(s: str) -> bool:
    return any([x.isalpha() for x in s])


def __tokenize_word(word: str, morph: MorphAnalyzer) -> str:
    return morph.parse(word)[0].normal_form


def normalize_str(s: str, morph: MorphAnalyzer) -> str:
    splitted: list[str] = [x.lower() for x in __split_str(s) if x and __has_alpha(x)]
    stop_words: list[str] = nltk.corpus.stopwords.words('russian')
    morphed: list[str] = [__tokenize_word(x, morph) for x in splitted if x not in stop_words]
    return ' '.join(morphed)


def transform_questions(morph: MorphAnalyzer, session: Session) -> None:
    for question in session.query(Question).all():
        transformed_question = normalize_str(question.raw, morph)
        question.transformed = transformed_question
        session.add(question)
