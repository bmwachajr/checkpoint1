"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
from room import room, livingSpace, officeSpace

class dojo:
    """Andela facility called the Dojo"""
    def __init__(self):
        self.all_offices = []
        self.all_livingSpaces = []
        self.all_rooms = []
        self.avialable_rooms = []
        self.all_fellows = []
        self.all_staff = []
        self.unallocated_people = []

    def create_room(self, room_name, room_type):
        """Add a room and return object"""
        if room_type.lower() == 'office':
            new_office = officeSpace(room_name)
            self.all_rooms.append(new_office)
            self.all_offices.append(new_office)
            self.avialable_rooms.append(new_office)
            return new_office

        if room_type.lower == 'livingspace':
            new_livingspace = livingSpace(room_name)
            self.all_rooms.append(new_livingspace)
            self.all_livingSpaces(new_livingspace)
            self.avialable_rooms.append(new_livingspace)
            return new_livingspace
