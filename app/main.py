from allocation_file_reader import AllocationFileReader
from amity import Amity
from persons.fellow import Fellow
from persons.staff import Staff
from persons.person import Person
from rooms.livingspace import LivingSpace
from rooms.office import Office
from rooms.room import Room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base

def main():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    room1 = Office('Taju')
    person1 = Fellow(name="Pyjac")

    room1.room_occupants.append(person1)
    session.add(room1)
    session.commit()
    print person1.id

    # room2 = LivingSpace('Taju1')
    #session.add(room2)

    #office = session.query(Room).all()
    #print(office)

    # allocation_reader = AllocationFileReader('allocation.txt')
    # amity = Amity("Amity")
    #
    # amity.add_room(LivingSpace("Poplar"))
    # amity.add_room(Office("M55 F3"))
    #
    # for person_info in allocation_reader.get_allocation_list():
    #     person_info = person_info.split()
    #     if len(person_info) < 3:
    #         raise ValueError('Invalid Input Data')
    #     if person_info[2] not in ('FELLOW', 'STAFF'):
    #         raise ValueError('Invalid Input Data. Person must be either a FELLOW or STAFF')
    #     if person_info[2] == 'FELLOW':
    #         if len(person_info) > 3:
    #             person = Fellow(" ".join(person_info[:2]), person_info[3])
    #         else:
    #             person = Fellow(" ".join(person_info[:2]))
    #     else:
    #         person = Staff(" ".join(person_info[:2]))
    #     amity.allocate_rooms(person)
    # amity.print_allocations()
    # amity.print_unallocated_persons()

if __name__ == '__main__':
    main()
