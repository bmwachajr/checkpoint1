"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""

class person:
    """Employee at andela"""
    def __init__(self, person_name, person_type):
        self.person_name = person_name
        self.person_type = person_type
        self.officeSpace = 'Unallocated'

class fellow(person):
    """Fellows at the Dojo"""
    def __init__(self, fellow_name, wants_acomodation):
        super().__init__(fellow_name, person_type='fellow')

        if wants_acomodation = "Y":
            self.livingSpace = 'Unallocated'
        else:
            self.livingSpace = None
