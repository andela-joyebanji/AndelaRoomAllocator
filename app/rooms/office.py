from room import Room


class Office(Room):
    capacity = 6
    __mapper_args__ = {
        'polymorphic_identity': 'OFFICE'
    }

