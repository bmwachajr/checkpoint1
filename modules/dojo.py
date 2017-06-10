"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
from room import room, livingSpace, officeSpace
from person import person, fellow, staff

class dojo:
    """Andela facility called the Dojo"""
    def __init__(self):
        self.all_offices = []
        self.all_livingSpaces = []
        self.all_rooms = []
        self.avialable_offices = []
        self.avialable_livingspaces = []
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

    def add_person(self, person_name, person_type, wants_acomodation):
        """Add an employee at the dojo """
        if person_type.lower() == "fellow":
            new_fellow = fellow(person_name)
            self.all_fellows.append(new_fellow)

            #allocate office and livingSpace
            new_fellow.officeSpace = self.allocate_officeSpace(new_fellow)
            if wants_acomodation.lower() == "y":
                new_fellow.livingSpace = self.allocate_livingSpace(new_fellow)
            return new_fellow

        if person_type.lower() == "staff":
            new_staff = staff(person_name)
            self.all_staff.append(new_staff)

            #allocate office and livingSpace
            new_staff.officeSpace = self.allocate_officeSpace(new_staff)
            return new_staff

    def allocate_officeSpace(self, new_person):
        """Allocate a random office"""
        if len(self.avialable_offices) > 0:
            random_room = random(self.avialable_offices)
            random_room.occupants.append(new_person)
            return(random_room.room_name)
        else:
            self.unallocated_people.append(new_person)
            return 'Unallocated'
