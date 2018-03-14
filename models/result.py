from .database_tools import Base
from sqlalchemy import Column, Integer, String, Float, Text

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    sector = Column(Text)
    type = Column(Text)
    machine_learning_technique = Column(Text)
    date = Column(Text)
    prediction = Column(Float)
    result = Column(Integer)
    difference = Column(Float)
