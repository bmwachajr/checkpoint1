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
        self.assertTrue('blue_office')
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_add_fellow_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'N')
        self.assertTrue(new_fellow)

    def test_add_fellow_without_rooms_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'N')
        self.assertEqual(new_fellow.officeSpace, "Unallocated")
        self.assertEqual(new_fellow.livingSpace, None)

    def test_add_staff_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertTrue(new_staff)

    def test_add_staff_without_offices_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertEqual(new_staff.officeSpace, "Unallocated")

if __name__ == "__main__":
  unittest.main()
