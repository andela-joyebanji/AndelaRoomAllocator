import unittest
from app.amity import Amity
from app.rooms.livingspace import LivingSpace
from app.rooms.office import Office
from app.persons.staff import Staff
from app.persons.fellow import Fellow


class TestFacility(unittest.TestCase):

    def setUp(self):
        self.facility = Amity("Amity")
        self.facility.add_room(LivingSpace("Poplar"))
        self.facility.add_room(Office("M55 F1"))

    def test_facility_rooms_empty_on_create(self):
        facility = Amity("Amity")
        self.assertEqual(0, len(facility.rooms))

    def test_facility_add_room(self):
        self.facility.add_room(LivingSpace("Coco"))
        self.assertEqual(3, len(self.facility.rooms))

        self.facility.add_room(LivingSpace("Ram"))
        self.assertEqual(4, len(self.facility.rooms))

    def test_facility_add_room_raise_error_if_name_exist(self):
        self.assertRaises(ValueError, self.facility.add_room, LivingSpace("Poplar"))

    def test_facility_allocate_staff_room(self):
        pyjac = Staff("Pyjac")
        allocated_rooms = self.facility.allocate_rooms(pyjac)
        self.assertIsInstance(allocated_rooms, Office)

    def test_facility_allocate_fellow_only_to_office_room(self):
        pyjac = Fellow("Pyjac")
        allocated_rooms = self.facility.allocate_rooms(pyjac)
        self.assertIsInstance(allocated_rooms[0], Office)

    def test_facility_allocate_fellow_office_and_living_room(self):
        pyjac = Fellow("Pyjac", 'Y')
        allocated_rooms = self.facility.allocate_rooms(pyjac)
        self.assertEquals(2, len(allocated_rooms))
        self.assertIsInstance(allocated_rooms[1], LivingSpace)
        self.assertIsInstance(allocated_rooms[0], Office)

    def test_facility_allocate_person_twice_raise_error(self):
        pyjac = Fellow("Pyjac", 'Y')
        self.facility.allocate_rooms(pyjac)
        self.assertRaises(ValueError, self.facility.allocate_rooms, pyjac)
        pyjac = Staff("Pyjac")
        self.assertRaises(ValueError, self.facility.allocate_rooms, pyjac)

    def test_facility_allocate_allocates_no_living_room_to_fellow_when_filled(self):
        pyjac = Fellow("Pyjac", 'Y')
        mayowa = Fellow("Mayowa", 'Y')
        jacob = Fellow("Jacob", 'Y')
        oyebanji = Fellow("Oyebanji", 'Y')
        taju = Fellow("Taju", 'Y')

        self.facility.allocate_rooms(pyjac)
        self.facility.allocate_rooms(mayowa)
        self.facility.allocate_rooms(jacob)

        # The fourth person gets the last available living room
        allocated_rooms = self.facility.allocate_rooms(oyebanji)
        self.assertEqual(2, len(allocated_rooms))
        self.assertIsInstance(allocated_rooms[1], LivingSpace)

        allocated_rooms = self.facility.allocate_rooms(taju)
        self.assertEqual(1, len(allocated_rooms))
        self.assertNotIsInstance(allocated_rooms[0], LivingSpace)

    def test_facility_allocate_returns_none_staff_when_office_rooms_filled(self):
        pyjac = Staff("Pyjac")
        mayowa = Staff("Mayowa")
        jacob = Staff("Jacob")
        oyebanji = Staff("Oyebanji")
        taju = Staff("Taju")
        salako = Staff("Salako")
        ibrahim = Staff("Ibrahim")

        self.facility.allocate_rooms(pyjac)
        self.facility.allocate_rooms(mayowa)
        self.facility.allocate_rooms(oyebanji)
        self.facility.allocate_rooms(taju)
        self.facility.allocate_rooms(salako)

        # The sixth person gets the last available office room
        allocated_room = self.facility.allocate_rooms(jacob)
        self.assertIsInstance(allocated_room, Office)

        allocated_rooms = self.facility.allocate_rooms(ibrahim)
        self.assertEqual(None, allocated_rooms)

    def test_facility_allocate_return_none_when_all_rooms_are_filled(self):
        pyjac = Fellow("Pyjac", 'Y')
        mayowa = Fellow("Mayowa", 'Y')
        jacob = Fellow("Jacob", 'Y')
        oyebanji = Fellow("Oyebanji", 'Y')
        taju = Fellow("Taju", 'Y')
        salako = Fellow("Salako", 'Y')
        ibrahim = Fellow("Ibrahim", 'Y')

        self.facility.allocate_rooms(pyjac)
        self.facility.allocate_rooms(mayowa)
        self.facility.allocate_rooms(oyebanji)
        self.facility.allocate_rooms(taju)
        self.facility.allocate_rooms(salako)

        # The sixth person gets the last available office room
        allocated_room = self.facility.allocate_rooms(jacob)
        self.assertIsInstance(allocated_room[0], Office)

        allocated_rooms = self.facility.allocate_rooms(ibrahim)
        self.assertEqual(None, allocated_rooms)

    def test_print_allocations(self):
        pyjac = Fellow("Pyjac", 'Y')
        self.facility.allocate_rooms(pyjac)
        self.facility.print_allocations()

if __name__ == '__main__':
    unittest.main()

