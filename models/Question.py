from sqlalchemy import Column, Integer, VARCHAR

from globals import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    raw = Column(VARCHAR, nullable=False)
    transformed = Column(VARCHAR, nullable=True)

    def __repr__(self):
        return f"{self.id}: {self.raw}"
