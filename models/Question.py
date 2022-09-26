from sqlalchemy import Column, Integer, VARCHAR, Enum
import enum
from globals import Base


class AnswerType(enum.Enum):
    YES_NO = 1
    TEXT = 2
    RANGE_5 = 3
    RANGE_10 = 4
    CUSTOM = 5
    RANGE_7 = 6


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    raw = Column(VARCHAR, nullable=False)
    transformed = Column(VARCHAR, nullable=True)
    answer_type = Column(Enum(AnswerType), default=AnswerType.YES_NO)

    def __repr__(self):
        return f"{self.id}: {self.raw}"
