"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
import random, sqlite3, pickle
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
            room_id = len(self.all_rooms) +1
            new_office = officeSpace(room_id, room_name)
            self.all_rooms.append(new_office)
            self.all_offices.append(new_office)
            self.avialable_offices.append(new_office)
            return new_office

        if room_type.lower() == 'livingspace':
            room_id = len(self.all_rooms) +1
            new_livingspace = livingSpace(room_id, room_name)
            self.all_rooms.append(new_livingspace)
            self.all_livingSpaces.append(new_livingspace)
            self.avialable_livingspaces.append(new_livingspace)
            return new_livingspace

    def add_person(self, person_name, person_type, wants_acomodation):
        """Add an employee at the dojo """
        for person in self.all_employees:
            #Check if employee is added, retun that object
            if person_name.lower() == person.person_name.lower():
                return person

        if person_type.lower() == "fellow":
            new_person_id = len(self.all_employees) + 1
            new_fellow = fellow(new_person_id, person_name)
            self.all_fellows.append(new_fellow)
            self.all_employees.append(new_fellow)

            #allocate office and livingSpace
            new_fellow.officeSpace = self.allocate_officeSpace(new_fellow)
            if wants_acomodation == None or wants_acomodation.lower() == 'n':
                return new_fellow
            elif wants_acomodation.lower() == "y":
                new_fellow.livingSpace = self.allocate_livingSpace(new_fellow)
                return new_fellow

        if person_type.lower() == "staff":
            new_person_id = len(self.all_employees) + 1
            new_staff = staff(new_person_id, person_name)
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


        #reallocate person
        if len(new_room.occupants) < 6:
            new_room.occupants.append(person)
            if current_room != None:
                current_room.occupants.remove(person)
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
        #create an output file , else set to none
        if output_file.lower() != "":
            with open("../outputs/" + str(output_file) , "w+") as output_file:
                #print details to file
                for room in self.all_rooms:
                    print(room.room_name + " - " + room.room_type, file = output_file, flush = True)
                    print("........................................", file = output_file, flush = True)
                    for person in room.occupants:
                        print(person.person_name + " (" +(person.person_type) + ")", file = output_file, flush = True)

    def print_unallocated(self, output_file):
        """Print unallocated people to file"""
        #create an output file , else set to none
        if output_file.lower() != "":
            with open("../outputs/" + output_file, "w+") as output_file:
                #write infromation to fileprint("People unallocated office", file = output_file, flush = True)
                print(".......................................", file = output_file, flush = True)
                for  person in self.unallocated_offices:
                    print(person.person_name + " (" + person.person_type + ")", file = output_file, flush = True)
                print("Fellows unallocated livingspaces", file = output_file, flush = True)
                print(".......................................", file = output_file, flush = True)
                for  person in self.unallocated_livingspaces:
                    print(person.person_name + " (" + person.person_type + ")", file = output_file, flush = True)


    def print_room(self, room_name):
        """print people allocated to room"""
        room = self.find_room(room_name)

        if room == None:
            return None
        else:
            return room


    def save_state(self, database_name):
        """ persist all data to sqlte database"""
        #create pickle of dojo object
        with open("../database/dojoObject.file", "wb") as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

        #open database ctreate a table and save file
        if database_name == "":
            database_name = "database.db"

        db = sqlite3.connect("../database/" + str(database_name))
        self.save_dojo(db)
        db.commit()
        db.close()
        return True

    def save_dojo(self, db):
        if db == None:
            return("Sorry database connection failed")

        #create database table
        db.execute('''CREATE TABLE if not exists Dojo
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL,
                    FILE BLOB)''')

        #Insert file into database
        with open("../database/dojoObject.file", "rb") as input_file:
            db.execute('''INSERT INTO dojo(NAME, FILE)
                    VALUES(?,?)''', ("DOJO BACKUP", sqlite3.Binary(input_file.read())))
