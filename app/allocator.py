"""Amity Room Allocation System .

Usage:
  allocator.py load_people
  allocator.py create_room (<room_name> TYPE) ...
  allocator.py print_room <room_name>
  allocator.py add_person <person_name> (FELLOW | STAFF) [<wants_accommodation>]
  allocator.py reallocate_person <person_identifier> <new_room_name>
  allocator.py print_allocations [-o FILENAME]
  allocator.py print_unallocated [-o FILENAME]
  allocator.py save_state [--db=sqlite_database]
  allocator.py load_state <sqlite_database>
  allocator.py (-h | --help)
"""
from docopt import docopt
from allocation_file_reader import AllocationFileReader
from amity import Amity
from rooms.room import Room
from rooms.livingspace import LivingSpace
from rooms.office import Office
from persons.fellow import Fellow
from persons.staff import Staff
from persons.person import Person
from app import (Base, session, engine)
import sys


class Allocator(object):

    @staticmethod
    def get_amity():
        return session.query(Amity).filter(Amity.name == 'Amity').first()

    @staticmethod
    def load_people():
        Base.metadata.create_all(engine)
        allocation_reader = AllocationFileReader('allocation.txt')
        amity = Amity(name="Amity")
        amity.add_room(LivingSpace(name="Poplar"))
        amity.add_room(Office(name="M55 F3"))
        session.add(amity)
        session.commit()
        for person_info in allocation_reader.get_allocation_list():
            person_info = person_info.split()
            if len(person_info) < 3:
                raise ValueError('Invalid Input Data')
            if person_info[2] not in ('FELLOW', 'STAFF'):
                raise ValueError('Invalid Input Data. Person must be either a FELLOW or STAFF')
            if person_info[2] == 'FELLOW':
                if len(person_info) > 3:
                    person = Fellow(name=" ".join(person_info[:2]), accommodation=person_info[3])
                else:
                    person = Fellow(name=" ".join(person_info[:2]))
            else:
                person = Staff(name=" ".join(person_info[:2]))
            amity.allocate_rooms(person)
            session.add(amity)
            session.commit()

    @staticmethod
    def create_room(params):
        amity = Allocator.get_amity()
        for key, room in enumerate(params['<room_name>']):
            amity.add_room(Office(name=room)) if params['TYPE'][key] == 'OFFICE' else amity.add_room(LivingSpace(name=room))
            session.add(amity)
            session.commit()
        print "Room(s) created"

    @staticmethod
    def add_person(params):
        amity = Allocator.get_amity()
        if params['FELLOW']:
            if params['<wants_accommodation>'] and params['<wants_accommodation>'] == 'Y':
                person = Fellow(name=params['<person_name>'], accommodation='Y')
            else:
                person = Fellow(name=params['<person_name>'])
        else:
            person = Staff(name=params['<person_name>'])
        amity.allocate_rooms(person)
        session.add(amity)
        session.commit()

    @staticmethod
    def print_room(params):
        room = session.query(Room).filter(Room.name.ilike(params['<room_name>'][0])).first()
        if room:
            if room.has_occupants():
                print "ROOM OCCUPANTS\n{}".format("="*20)
                for person in room.room_occupants:
                    print person.name
            else:
                print "Room has no occupants"
        else:
            print "Room does not exist"

    @staticmethod
    def print_allocations(params):
        amity = Allocator.get_amity()
        output = Allocator.get_output(params)
        amity.print_allocations(output)
        output.close()

    @staticmethod
    def print_unallocated(params):
        amity = Allocator.get_amity()
        output = Allocator.get_output(params)
        amity.print_unallocated_persons(output)
        output.close()

    @staticmethod

    def reallocate_person(params):
        """
        allocator.py reallocate_person <person_identifier> <new_room_name>
        """
        amity = Allocator.get_amity()
        room = session.query(Room).filter(Room.name.ilike(params['<new_room_name>'])).first()
        person = session.query(Person).filter(Person.name.ilike(params['<person_identifier>'])).first()
        if not room:
            print "{} does not exist".format(params['<new_room_name>'])
            return False
        if room.filled():
            print "{} is filled".format(params['<new_room_name>'])
            return False
        if not person:
            print "{} does not exist".format(params['<person_identifier>'])
            return False
        if room.is_room_occupant(person):
            print "{} is already a occupant of {}".format(params['<person_identifier>'], params['<new_room_name>'])
            return False
        amity.reallocate_person(room, person)
        session.add(amity)
        session.commit()
        print "{} successfully relocated.".format(person.name)

    @staticmethod
    def get_output(params):
        return open(params['FILENAME'], 'w') if params['-o'] else sys.stdout


def main(params):
    allocator = Allocator()
    for key, value in params.items():
        if value is True and key[0] != '-':
            method = getattr(allocator, key)
            method(params)
            break


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Allocator 1.0', options_first=False)
    main(arguments)




