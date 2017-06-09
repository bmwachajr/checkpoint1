"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""

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
