"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
import random
from random import choice
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
        self.all_employees = []
        self.unallocated_offices = []
        self.unallocated_livingspaces = []

    def create_room(self, room_name, room_type):
        """Add a room and return object"""
        for room in self.all_rooms:
            #check if room has already been added, return object
            if room_name.lower() == room.room_name.lower():
                return room

        if room_type.lower() == 'office':
            new_office = officeSpace(room_name)
            self.all_rooms.append(new_office)
            self.all_offices.append(new_office)
            self.avialable_offices.append(new_office)
            return new_office

        if room_type.lower() == 'livingspace':
            new_livingspace = livingSpace(room_name)
            self.all_rooms.append(new_livingspace)
            self.all_livingSpaces.append(new_livingspace)
            self.avialable_livingspaces.append(new_livingspace)
            return new_livingspace

    def add_person(self, person_name, person_type, wants_acomodation):
        """Add an employee at the dojo """
        for person in self.all_employees:
            #Check if employee is added, retun that object
            if person_name.lower() == person.person_name:
                return person

        if person_type.lower() == "fellow":
            new_fellow = fellow(person_name)
            self.all_fellows.append(new_fellow)
            self.all_employees.append(new_fellow)

            #allocate office and livingSpace
            new_fellow.officeSpace = self.allocate_officeSpace(new_fellow)
            if wants_acomodation.lower() == "y":
                new_fellow.livingSpace = self.allocate_livingSpace(new_fellow)
            return new_fellow

        if person_type.lower() == "staff":
            new_staff = staff(person_name)
            self.all_staff.append(new_staff)
            self.all_employees.append(new_staff)

            #allocate office and livingSpace
            new_staff.officeSpace = self.allocate_officeSpace(new_staff)
            return new_staff

    def allocate_officeSpace(self, new_occupant):
        """Allocate a random office"""
        if len(self.avialable_offices) > 0:
            random_office = choice(self.avialable_offices)
            random_office.occupants.append(new_occupant)

            #remove room from avialable rooms is occupants are 6
            if len(random_office.occupants) > 5:
                self.avialable_offices.remove(random_office)

            return(random_office.room_name)
        else:
            self.unallocated_offices.append(new_occupant)
            return "Unallocated"

    def allocate_livingSpace(self, new_occupant):
        """Allocate a living space"""
        if len(self.avialable_livingspaces) > 0:
            random_livingspace = choice(self.avialable_livingspaces)
            random_livingspace.occupants.append(new_occupant)

            #remove room from avialable room list if occupants are 4
            return (random_livingspace.room_name)
        else:
            self.unallocated_livingspaces.append(new_occupant)
            return "Unallocated"

    def reallocate_person(self, person_name, new_room_name):
        """reallocate person to new room if its avialable"""
        person = self.find_person(person_name)
        new_room = self.find_room(new_room_name)

        if person == None:
            return("Person Not Found")
        elif new_room == None:
            return("Room Not Found")
        else:
            #find the current room they occupy
            if new_room.room_type == "officeSpace":
                current_room_name = person.officeSpace
            else:
                current_room_name = person.livingSpace
            current_room = self.find_room(current_room_name)

        if len(new_room.occupants) < 6:
            new_room.occupants.append(person)
            if current_room != None:
                current_room.occupants.remove(person)
            if new_room.room_type == "officeSpace":
                person.officeSpace = new_room.room_name
            else:
                person.livingSpace = new_room.room_name

    def find_person(self, person_name):
        """Search for an employee using their unique name"""
        for person in self.all_employees:
            if person.person_name.lower() == person_name.lower():
                return person
        return None

    def find_room(self, room_name):
        """search fro a room using its name"""
        for room in self.all_rooms:
            if room.room_name.lower() == room_name.lower():
                return room
        return None

    def load_people(self, path_to_file):
        """Load people from a text file"""
        with open(path_to_file, 'r') as file:
            for line in file:
                person_details = line.rstrip().split(' ')
                person_name = person_details[0] + " " + person_details[1]
                person_type = person_details[2]
                if len(person_details) == 4:
                    wants_accomodation = person_details[3]
                else:
                    wants_accomodation = ""
                self.add_person(person_name, person_type, wants_accomodation)

    def print_allocations(self, file_output):
        """Print persons allocated to each room"""
        #create an output file , else set to none
        if file_output.lower() == "y":
            output_file = open("allocations.txt", "w+")
        else:
            output_file = None

        for room in self.all_rooms:
            print(room.room_name + " - " + room.room_type, file = output_file, flush = True)
            print("........................................", file = output_file, flush = True)
            for person in room.occupants:
                print(person.person_name + " (" +(person.person_type) + ")", file = output_file, flush = True)

    def print_unallocated(self):
        """Print unallocated people"""
        print("People unallocated office")
        print(".......................................")
        for  person in self.unallocated_offices:
            print(person.person_name + " (" + person.person_type + ")")

        print("Fellows unallocated livingspaces")
        print(".......................................")
        for  person in self.unallocated_livingspaces:
            print(person.person_name + " (" + person.person_type + ")")

    def print_room(self, room_name):
        """print people allocated to room"""
        room = self.find_room(room_name)

        if room == None:
            return None
        print(room.room_name + " " + room.room_type)
        print("......................................")
        for person in room.occupants:
            print(person.person_name + " (" + person.person_type + ")")
