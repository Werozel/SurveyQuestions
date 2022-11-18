from globals import session_factory
from models.Question import Question, AnswerType


def populate_from_file(file_name: str, answer_type: AnswerType) -> None:
    with session_factory() as session:
        with open(file_name, "r", encoding="utf-8") as fin:
            questions = map(lambda x: x.strip(), fin.readlines())
            for question in questions:
                session.add(Question(raw=question, answer_type=answer_type))
        session.commit()


def remove_all_questions() -> None:
    with session_factory() as session:
        for question in session.query(Question).all():
            session.delete(question)
        session.commit()
