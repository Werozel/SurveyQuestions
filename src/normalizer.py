from globals import session_factory
from pymorphy2 import MorphAnalyzer
from models.Question import Question
import re
import nltk


def split_str(s: str) -> list[str]:
    return re.split("[,.-;!?_: ]", s)


def has_alpha(s: str) -> bool:
    return any([x.isalpha() for x in s])


def tokenize_word(word: str, morph: MorphAnalyzer) -> str:
    return morph.parse(word)[0].normal_form


def normalize_str(s: str, morph: MorphAnalyzer) -> str:
    splitted: list[str] = [x.lower() for x in split_str(s) if x and has_alpha(x)]
    morphed: list[str] = [tokenize_word(x, morph) for x in splitted]
    return ' '.join(morphed)


def transform_questions(morph: MorphAnalyzer) -> None:
    session = session_factory()
    for question in session.query(Question).all():
        transformed_question = normalize_str(question.raw, morph)
        question.transformed = transformed_question
        session.add(question)
    session.commit()
    session.close()


if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")

    print(normalize_str("Сделал/сделаю это - то, да! Сё.", MorphAnalyzer()))
