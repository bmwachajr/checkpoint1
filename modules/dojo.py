"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
import sqlite3
import pickle
from random import choice
from room import livingSpace, officeSpace
from person import fellow, staff


class dojo(object):
    """Andela facility called the Dojo"""
    def __init__(self):
        self.all_offices = []
        self.all_livingSpaces = []
        self.all_rooms = []
        self.avialable_offices = []
        self.avialable_livingspaces = []
        self.all_employees = []
        self.unallocated_offices = []
        self.unallocated_livingspaces = []

    def create_room(self, room_name, room_type):
        """Add a room and return object"""
        for room in self.all_rooms:
            # check if room has already been added, return object
            if room_name.lower() == room.room_name.lower():
                return (room.room_name + " already exists")

        if room_type.lower() == 'office':
            room_id = len(self.all_rooms) + 1
            new_office = officeSpace(room_id, room_name)
            self.all_rooms.append(new_office)
            self.all_offices.append(new_office)
            self.avialable_offices.append(new_office)

            # return receipt of success or failure
            if new_office is not None:
                return ("An Office " + new_office.room_name + " was successfully created")
            else:
                return("The office was not created successfully")

        if room_type.lower() == 'livingspace':
            room_id = len(self.all_rooms) + 1
            new_livingspace = livingSpace(room_id, room_name)
            self.all_rooms.append(new_livingspace)
            self.all_livingSpaces.append(new_livingspace)
            self.avialable_livingspaces.append(new_livingspace)

            # return receipt of success or failure
            if new_livingspace is not None:
                return ("A livingspace " + new_livingspace.room_name + "was created successfully")
            else:
                return("The Livingspace was not created successfully")

    def add_person(self, person_name, person_type, wants_acomodation):
        """Add an employee at the dojo """
        for person in self.all_employees:
            # Check if employee is added, retun that object
            if person_name.lower() == person.person_name.lower():
                return ("A person with the name " + person.person_name + " already exists")

        if person_type.lower() == "fellow":
            new_person_id = len(self.all_employees) + 1
            new_fellow = fellow(new_person_id, person_name)
            self.all_employees.append(new_fellow)

            # allocate office and livingSpace
            new_fellow.officeSpace = self.allocate_officeSpace(new_fellow)
            if wants_acomodation is None or wants_acomodation.lower() == 'n':
                return new_fellow
            elif wants_acomodation.lower() == "y":
                new_fellow.livingSpace = self.allocate_livingSpace(new_fellow)
                return ("A fellow called " + new_fellow.person_name + " was created successfully\n"+
                        "Fellow " + new_fellow.person_name + " was allocated the Office " + new_fellow.officeSpace +"\n"+
                        "Fellow " + new_fellow.person_name + " was allocated a livindspace " + new_fellow.livingSpace)

        if person_type.lower() == "staff":
            new_person_id = len(self.all_employees) + 1
            new_staff = staff(new_person_id, person_name)
            self.all_employees.append(new_staff)

            # allocate office and livingSpace
            new_staff.officeSpace = self.allocate_officeSpace(new_staff)
            return ("A staff called " + new_staff.person_name + " was created successfully \n"+
                    "Staff " + new_staff.person_name + " was allocated the office " + new_staff.officeSpace )

    def allocate_officeSpace(self, new_occupant):
        """Allocate a random office"""
        if len(self.avialable_offices) > 0:
            random_office = choice(self.avialable_offices)
            random_office.occupants.append(new_occupant.person_name)

            # remove room from avialable rooms is occupants are 6
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
            random_livingspace.occupants.append(new_occupant.person_name)

            # remove room from avialable room list if occupants are 4
            return (random_livingspace.room_name)
        else:
            self.unallocated_livingspaces.append(new_occupant)
            return "Unallocated"

    def reallocate_person(self, person_name, new_room_name):
        """reallocate person to new room if its avialable"""
        person = self.find_person(person_name)
        new_room = self.find_room(new_room_name)

        if person is None:
            return("Person Not Found")
        elif new_room is None:
            return("Room Not Found")
        elif person.person_type.lower() == "staff" and new_room.room_type == "livingSpace":
            return("Cannot assign a staff to a Livingspace")
        else:
            # find the current room they occupy
            if new_room.room_type == "officeSpace":
                current_room_name = person.officeSpace
            else:
                current_room_name = person.livingSpace
            current_room = self.find_room(current_room_name)

        # reallocate person
        if len(new_room.occupants) < 6:
            new_room.occupants.append(person.person_name)
            if current_room is not None:
                current_room.occupants.remove(person.person_name)
            if new_room.room_type == "officeSpace":
                person.officeSpace = new_room.room_name
            else:
                person.livingSpace = new_room.room_name
            return person

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

    def load_people(self, file_name):
        """Load people from a text file"""
        loaded_people = []
        with open(("../inputs/" + file_name), 'r') as file:
            for line in file:
                person_details = line.rstrip().split(' ')
                person_name = person_details[0] + " " + person_details[1]
                person_type = person_details[2]
                if len(person_details) == 4:
                    wants_accomodation = person_details[3]
                else:
                    wants_accomodation = ""
                new_person = self.add_person(person_name, person_type, wants_accomodation)
                loaded_people.append(new_person)
            return loaded_people

    def print_allocations(self, output_file):
        """Print persons allocated to each room to file"""
        # create an output file , else set to none
        if output_file.lower() != "":
            with open("../outputs/" + str(output_file), "w+") as output_file:
                # print details to file
                for room in self.all_rooms:
                    print(room.room_name + " - " + room.room_type, file=output_file, flush = True)
                    print("."*40, file=output_file, flush=True)
                    for person in room.occupants:
                        print(person, file=output_file, flush=True)

    def print_unallocated(self, output_file):
        """Print unallocated people to file"""
        #create an output file , else set to none
        if output_file.lower() != "":
            with open("../outputs/" + output_file, "w+") as output_file:
                # write infromation to file
                print("Unallocated office", file=output_file, flush=True)
                print("."*40, file=output_file, flush=True)
                for person in self.unallocated_offices:
                    print(person.person_name + " (" + person.person_type + ")", file=output_file, flush=True)
                print("Unallocated livingspaces", file=output_file, flush=True)
                print("."*40, file=output_file, flush=True)
                for person in self.unallocated_livingspaces:
                    print(person.person_name + " (" + person.person_type + ")", file=output_file, flush=True)

    def print_room(self, room_name):
        """print people allocated to room"""
        room = self.find_room(room_name)

        if room is None:
            return None
        else:
            return room

    def save_state(self, database_name):
        """ persist all data to sqlte database"""
        # create prickle of dojo object
        rooms_pickle = pickle.dumps(self.all_rooms)
        employees_pickle = pickle.dumps(self.all_employees)
        #dojo_pickle = pickle.dumps(self)
        #print(dojo_pickle)

        # open database and ctreate a table
        db = sqlite3.connect("../database/" + str(database_name))
        db.execute('''CREATE TABLE if not exists Dojo
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     EMPLOYEES TEXT NOT NULL,
                     ROOMS TEXT NOT NULL)''')

        # Insert file into database
        db.execute('''INSERT INTO dojo(EMPLOYEES, ROOMS)
                     VALUES(?,?)''', (employees_pickle, rooms_pickle))

        db.commit()
        db.close()

    def load_state(self, database_name):
        """Restore all data to the application"""
        # retrieve file from database
        db = sqlite3.connect("../database/" + str(database_name))
        cursor = db.cursor()
        cursor.execute('''SELECT EMPLOYEES, ROOMS FROM Dojo
                    ORDER BY ID DESC
                    LIMIT 1''')
        employee_pickle, rooms_pickle = cursor.fetchone()
        self.all_rooms = pickle.loads(rooms_pickle)
        self.all_employees = pickle.loads(employee_pickle)
        self.room_restore()
        self.employee_restore()

    def room_restore(self):
        for room in self.all_rooms:
            print(room.room_name + " " + room.room_type)
            # appende to correct room list
            if room.room_type.lower() == "officespace":
                self.all_offices.append(room)
                if len(room.occupants) < 6:
                    self.avialable_offices.append(room)
            else:
                self.all_livingSpaces.append(room)
                if len(room.occupants) < 4:
                    self.avialable_offices.append(room)

    def employee_restore(self):
        """ restores person to the right lists """
        for person in self.all_employees:
            if person.officeSpace == "Unallocated":
                self.unallocated_offices.append(person)

            if person.person_type == "fellow":
                if person.livingSpace == "Unallocated":
                    self.unallocated_livingspaces.append(person)
