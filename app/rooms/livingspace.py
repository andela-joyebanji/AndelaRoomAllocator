from room import Room


class LivingSpace(Room):
    capacity = 4
    __mapper_args__ = {
        'polymorphic_identity': 'LIVING'
    }

