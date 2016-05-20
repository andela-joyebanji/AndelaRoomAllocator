

class AllocationFileReader(object):

    person_allocation_list = []

    def __init__(self, filename):
        with open(filename, 'r') as allocation_file:
            self.person_allocation_list = allocation_file.readlines()

    def get_allocation_list(self):
        return self.person_allocation_list
