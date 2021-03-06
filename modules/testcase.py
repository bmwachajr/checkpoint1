"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""

import unittest
from unittest import TestCase
import sqlite3
from dojo import dojo
from person import person, fellow, staff

class testCasesDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = dojo()

    def test_create_room_successfully(self):
        initial_room_count = len(self.dojo.all_rooms)
        blue_office = self.dojo.create_room("Blue", "Office")
        new_livingSpace = self.dojo.create_room("St. Catherines", "livingSpace")
        re_add_livingSpace = self.dojo.create_room("St. Catherines", "livingSpace")
        self.assertTrue('blue_office')
        self.assertTrue('new_livingSpace')
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 2)

    def test_add_fellow_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'N')
        self.assertTrue(new_fellow)
        re_add_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'N')
        self.assertIn("already exists", re_add_fellow)

    def test_add_fellow_without_rooms_successfully(self):
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", 'Y')
        self.assertIn("Office Unallocated", new_fellow)
        self.assertIn("livindspace Unallocated", new_fellow)

    def test_add_staff_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertTrue(new_staff)

    def test_add_staff_without_offices_successfully(self):
        new_staff = self.dojo.add_person("Benjamin Wacha", "Staff", '')
        self.assertIn("office Unallocated", new_staff)

    def test_find_person(self):
        self.dojo.add_person("Benjamin Wacha", "Staff", '')
        person = self.dojo.find_person("Benjamin Wacha")
        self.assertEqual(person.person_name, "Benjamin Wacha")
        self.assertEqual(self.dojo.find_person("Eugene Emron"), None)


    def test_allocates_officeSpace_successfully(self):
        new_office = self.dojo.create_room("Oculus", "Office")
        new_staff = self.dojo.add_person("Josh Mpaka", "Staff","")
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", "Y")
        self.assertIn("Oculus", new_staff)
        self.assertIn("Oculus", new_fellow)

    def test_allocates_livingSpace_successfully(self):
        new_office = self.dojo.create_room("Oculus", "livingspace")
        new_fellow = self.dojo.add_person("Benjamin Wacha", "Fellow", "Y")
        self.assertIn("Oculus", new_fellow)

    def test_reallocate_person_successfully(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.add_person("Albert Emron", "Staff", "")
        new_staff = self.dojo.find_person("Albert Emron")
        self.assertEqual(new_staff.officeSpace, "Dakar")
        self.dojo.create_room("Jinja", "Office")
        self.dojo.reallocate_person("Albert Emron", "Jinja")
        self.dojo.reallocate_person("Benjamin Wacha", "Oculus")#Occculus doesnt exit
        self.assertEqual(new_staff.officeSpace, "Jinja")
        self.assertEqual(len(self.dojo.all_rooms), 2)

    def test_reallocate_Unallocated_person_successfully(self):
        new_staff = self.dojo.add_person("Albert Emron", "Staff", "")
        self.assertIn("office Unallocated", new_staff)
        self.dojo.create_room("Jinja", "Office")
        self.dojo.reallocate_person("Albert Emron", "Jinja")
        new_staff = self.dojo.find_person("Albert Emron")
        self.assertEqual(new_staff.officeSpace, "Jinja", new_staff)

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
        self.dojo.print_allocations("file.txt")

    def test_print_allocations_file_output(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.create_room("St. Catherines", "livingspace")
        self.assertTrue("St. Catherines")
        self.dojo.load_people('file.txt')
        self.assertEqual(len(self.dojo.all_employees), 7)
        self.assertEqual(len(self.dojo.all_rooms), 2)
        self.dojo.print_allocations("unallocated.txt")

    def test_print_untallocated(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.load_people('file.txt')
        self.assertEqual(len(self.dojo.unallocated_offices), 1)
        self.assertEqual(len(self.dojo.unallocated_livingspaces), 4)
        #self.dojo.print_unallocated("")

    def test_print_untallocated_file_output(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.load_people('file.txt')
        self.assertEqual(len(self.dojo.unallocated_offices), 1)
        self.assertEqual(len(self.dojo.unallocated_livingspaces), 4)
        self.dojo.print_unallocated("Y")

    def test_find_room(self):
        self.dojo.create_room("Dakar", "Office")
        self.dojo.load_people('file.txt')
        Dakar = self.dojo.find_room("Dakar")
        self.assertEqual(Dakar.room_name, "Dakar")
        self.assertEqual(len(Dakar.occupants), 6)
        #self.dojo.print_room("Dakar")
        #self.dojo.print_room("Oculus")

    def test_save_state(self):
        self.dojo.create_room("Dakar", "office")
        self.dojo.create_room("St.Catherine", "livingspace")
        self.dojo.load_people('file.txt')
        self.dojo.save_state("database.db")
        db = sqlite3.connect("../database/database.db")
        cursor = db.cursor()
        cursor.execute('''SELECT EMPLOYEES, ROOMS FROM dojo
                    ORDER BY ID DESC
                    LIMIT 1''')
        FILE = cursor.fetchall()
        self.assertFalse(FILE is None)

    def test_load_state(self):
        self.dojo.load_state("database.db")
        self.assertTrue(self.dojo.all_rooms)
        self.assertEqual(len(self.dojo.all_rooms), 2)


if __name__ == "__main__":
    unittest.main()
