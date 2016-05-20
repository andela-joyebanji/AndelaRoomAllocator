from person import Person


class Fellow(Person):
    __mapper_args__ = {'polymorphic_identity': 'FELLOW'}

    @property
    def wants_accommodation(self):
        return True if self.accommodation == 'Y' else False
