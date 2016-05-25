import random
import sys
import os

sys.path.insert(0, os.path.realpath('..'))

from rooms.office import Office
from rooms.room import Room
from rooms.livingspace import LivingSpace
from persons.person import Person
from persons.staff import Staff
from persons.fellow import Fellow

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime,
                        ForeignKey, Boolean)
from app import Base
from app import session

AvailableOfficeRooms = Table('available_office_rooms',
                             Base.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('facility_id', Integer, ForeignKey('facility.id')),
                             Column('room_id', Integer, ForeignKey('rooms.id')),
                             extend_existing=True
                             )
AvailableLivingRooms = Table('available_living_rooms',
                             Base.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('facility_id', Integer, ForeignKey('facility.id')),
                             Column('room_id', Integer, ForeignKey('rooms.id')),
                             extend_existing=True
                             )
FilledLivingRooms = Table('filled_living_rooms',
                          Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('facility_id', Integer, ForeignKey('facility.id')),
                          Column('room_id', Integer, ForeignKey('rooms.id')),
                          extend_existing=True
                          )

FilledOfficeRooms = Table('filled_office_rooms',
                          Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('facility_id', Integer, ForeignKey('facility.id')),
                          Column('room_id', Integer, ForeignKey('rooms.id')),
                          extend_existing=True
                          )

PersonRooms = Table('person_rooms',
                    Base.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('facility_id', Integer, ForeignKey('facility.id')),
                    Column('person_id', Integer, ForeignKey('persons.id')),
                    Column('room_id', Integer, ForeignKey('rooms.id')),
                    extend_existing=True
                    )

UnallocatedPersons = Table('unallocated_persons',
                           Base.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('facility_id', Integer, ForeignKey('facility.id')),
                           Column('person_id', Integer, ForeignKey('persons.id')),
                           extend_existing=True
                           )


class Amity(Base):
    __tablename__ = 'facility'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    available_office_rooms = relationship("Room", secondary=AvailableOfficeRooms)
    available_living_rooms = relationship("Room", secondary=AvailableLivingRooms)
    filled_living_rooms = relationship("Room", secondary=FilledLivingRooms)
    filled_office_rooms = relationship("Room", secondary=FilledOfficeRooms)
    person_rooms = relationship("Room", secondary=PersonRooms)
    unallocated_persons = relationship("Person", secondary=UnallocatedPersons)

    def __init__(self, name, rooms=None):
        super(Amity, self).__init__(name=name)

    @property
    def rooms(self):
        return self.merge_dicts(self.available_office_rooms,
                                self.available_living_rooms,
                                self.filled_living_rooms,
                                self.filled_office_rooms
                                )

    def merge_dicts(self, *dict_args):
        '''
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        '''
        result = []
        for dictionary in dict_args:
            result = dictionary[:] + result
        return result

    def add_room(self, room):
        if not isinstance(room, (Office, LivingSpace)):
            raise ValueError
        if self._room_exist(room.name):
            raise ValueError('Room Already Exist.')

        if isinstance(room, Office):
            if room.filled():
                self.filled_office_rooms.append(room)
            else:
                self.available_office_rooms.append(room)
        if isinstance(room, LivingSpace):
            if room.filled():
                self.filled_living_rooms.append(room)
            else:
                self.available_living_rooms.append(room)
        return True

    def _room_exist(self, room_name):
        return True if session.query(Room.name).filter(Room.name.ilike(room_name)).first() else False

    def get_person_room(self, person):
        return self.person_rooms.filter(Person.name == person.name).one()

    def allocate_rooms(self, person):
        if not isinstance(person, Person):
            raise ValueError
        if person.name in self.person_rooms:
            raise ValueError("{} Already Allocated a Room".format(person.name))
        return self._allocate_rooms(person)

    def _allocate_rooms(self, person):
        if isinstance(person, Staff) and self.available_office_rooms:
            return self._allocate_staff_room(person)
        if isinstance(person, Fellow):
            return self._allocate_fellow_rooms(person)
        return None

    def _allocate_fellow_rooms(self, person):
        if not self.available_office_rooms and not self.available_living_rooms:
            self.unallocated_persons.append(person)
            return None
        if self.available_office_rooms:
            self._allocate_staff_room(person)
        if self.available_living_rooms and person.wants_accommodation:
            self._allocate_living_room(person)
        #return self._person_rooms[person.name]

    def _allocate_living_room(self, person):
        room = self._allocate_to_random_room(person, self.available_living_rooms)
        if room.filled():
            self.available_living_rooms.remove(room)
            self.filled_living_rooms.append(room)

    def _allocate_staff_room(self, person):
        room = self._allocate_to_random_room(person, self.available_office_rooms)
        if room.filled():
            self.available_office_rooms.remove(room)
            self.filled_office_rooms.append(room)
        return room

    def _allocate_to_random_room(self, person, rooms):
        room = self._get_random_room(rooms)
        room.add_occupant(person)
        return room

    def reallocate_person(self, room, person):
        old_room = person.rooms.filter(Room.type == room.type).first()
        if old_room:
            old_room.remove_occupant(person)
        if old_room.type == "LIVING" and old_room in self.filled_living_rooms:
            self.filled_living_rooms.remove(old_room)
        if old_room in self.filled_office_rooms:
            self.filled_office_rooms.remove(old_room)
        return room.add_occupant(person)

    def print_allocations(self, output):
        for room in self.rooms:
            if room.has_occupants():
                output.write("\n".join([room.name, "-" * 37, ', '.join([person.name for person in room.room_occupants])]))
                output.write("\n")

    def print_unallocated_persons(self, output):
        output.write("\n".join(['UNALLOCATED PERSONS',
                         '-' * 37,
                         ', '.join([person.name for person in self.unallocated_persons])]) \
            if self.unallocated_persons else 'No unallocated Person.')

    def _get_random_room(self, rooms):
        return rooms[random.randint(0, len(rooms) - 1)]