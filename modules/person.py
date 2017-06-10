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
        self.officeSpace = "Unallocated"

class fellow(person):
    """A Fellow at the Dojo"""
    def __init__(self, fellow_name):
        person_type = "fellow"
        super().__init__(fellow_name, person_type)
        self.livingSpace = None

class staff(person):
    """A Staff member at the Dojo"""
    def __init__(self, staff_name):
        super().__init__(staff_name, person_type='staff')
