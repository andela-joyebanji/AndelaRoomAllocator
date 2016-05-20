from app import Base
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship


class Person(Base):
    __tablename__ = 'persons'
    __table_args__ = {'extend_existing': True, 'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55), unique=True)
    rooms = relationship("Room", secondary='room_occupants', lazy='dynamic')
    accommodation = Column(Enum('Y', 'N'))
    type = Column(Enum('FELLOW', 'STAFF'))
    __mapper_args__ = {
        'polymorphic_on': type
    }

