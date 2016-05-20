from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, ForeignKey)


engine = create_engine('sqlite:///storage.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class RoomOccupant(Base):
    __tablename__ = 'room_occupants'
    __table_args__ = {'extend_existing': True}
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
