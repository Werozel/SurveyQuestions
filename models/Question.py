from sqlalchemy import Column, Integer, VARCHAR, Enum
import enum
from globals import Base


class AnswerType(enum.Enum):
    CUSTOM = 0
    TEXT = 1
    YES_NO = 2
    RANGE_3 = 3
    RANGE_4 = 4
    RANGE_5 = 5
    RANGE_6 = 6
    RANGE_7 = 7
    RANGE_8 = 8
    RANGE_9 = 9
    RANGE_10 = 10


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    raw = Column(VARCHAR, nullable=False)
    transformed = Column(VARCHAR, nullable=True)
    answer_type = Column(Enum(AnswerType), default=AnswerType.YES_NO)

    def __repr__(self):
        return f"{self.id}: {self.raw}"
