import sys
import os
from app import (Base, RoomOccupant)
from sqlalchemy.types import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String)

sys.path.insert(0, os.path.realpath('../..'))


class Room(Base):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True, 'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    type = Column(Enum('LIVING', 'OFFICE'))
    room_occupants = relationship("Person", secondary='room_occupants', lazy='dynamic')
    capacity = 0
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'Room'
    }

    def get_capacity(self):
        return self.capacity

    def is_room_occupant(self, person):
        return self.room_occupants.filter(RoomOccupant.person_id == person.id).first()

    def filled(self):
        return self.room_occupants.count() == self.capacity

    def add_occupant(self, person):
        if self.filled():
            return False
        return self.room_occupants.append(person)

    def remove_occupant(self, person):
        return self.room_occupants.remove(person)

    def has_occupants(self):
        return self.room_occupants.count() > 0

    def __repr__(self):
        return self.__class__.__name__ + "(name='{self.name}', " \
               "type='{self.type}')".format(self=self)

if __name__ == "__main__":
    import os
    print os.path.realpath('../..')

