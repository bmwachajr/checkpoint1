"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""

class person:
    """Employee at andela"""
    def __init__(self, person_name, person_type, wants_acomodation):
        self.person_name = person_name
        self.person_type = person_type
        self.officeSpace = 'Unallocated'
