"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""

import unittest
from unittest import TestCase
from dojo import dojo
from person import person, fellow, staff

class testCasesDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = dojo()

    def test_create_room_successfully(self):
        initial_room_count = len(self.dojo.all_rooms)
        blue_office = self.dojo.create_room("Blue", "Office")
        new_livingSpace = self.dojo.create_room("St. Catherines", "livingSpace")
        self.assertTrue('blue_office')
        self.assertTrue('new_livingSpace')
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 2)

    def test_add_fellow_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'N')
        self.assertTrue(new_fellow)

    def test_add_fellow_without_rooms_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'Y')
        self.assertEqual(new_fellow.officeSpace, "Unallocated")
        self.assertEqual(new_fellow.livingSpace, "Unallocated")

    def test_add_staff_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertTrue(new_staff)

    def test_add_staff_without_offices_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertEqual(new_staff.officeSpace, "Unallocated")

    def test_allocates_officeSpace_successfully(self):
        new_office = self.dojo.create_room("Oculus", "Office")
        new_staff = self.dojo.add_person("Josh Mpaka", "Staff","")
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", "")
        self.assertEqual(new_staff.officeSpace, "Oculus")
        self.assertEqual(new_fellow.officeSpace, "Oculus")
        self.assertEqual(len(new_office.occupants), 2)

    def test_allocates_livingSpace_successfully(self):
        new_office = self.dojo.create_room("Oculus", "livingspace")
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", "Y")
        self.assertEqual(new_fellow.livingSpace, "Oculus")

    def test_reallocate_person_successfully(self):
        self.dojo.create_room("Dakar", "Office")
        new_staff = self.dojo.add_person("Albert Emron", "Staff", "")
        self.assertEqual(new_staff.officeSpace, "Dakar")
        self.dojo.create_room("Jinja", "Office")
        self.dojo.reallocate_person("Albert Emron", "Jinja")
        self.assertEqual(new_staff.officeSpace, "Jinja")
        self.assertEqual(len(self.dojo.all_rooms), 2)

    def test_reallocate_Unallocated_person_successfully(self):
        new_staff = self.dojo.add_person("Albert Emron", "Staff", "")
        self.assertEqual(new_staff.officeSpace, "Unallocated")
        other_office = self.dojo.create_room("Jinja", "Office")
        self.dojo.reallocate_person("Albert Emron", "Jinja")
        self.assertEqual(new_staff.officeSpace, "Jinja")

    def test_load_people_from_file(self):
        self.dojo.load_people('file.txt')
        self.assertEqual(len(self.dojo.all_employees), 7)

    def test_print_allocations(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.create_room("St. Catherines", "livingspace")
        self.assertTrue("St. Catherines")
        self.dojo.load_people('file.txt')
        self.assertEqual(len(self.dojo.all_employees), 7)
        self.assertEqual(len(self.dojo.all_rooms), 2)

    def test_print_untallocations(self):
        self.dojo.load_people('file.txt')
        self.assertEqual(len(seself.dojo.unallocated_offices), 7)
        self.assertEqual(len(self.dojo.unallocated_livingspaces, 4))

if __name__ == "__main__":
  unittest.main()
