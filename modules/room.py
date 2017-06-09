"""
Name        :  checkpoint1
Author      :  Benjamin Wacha
Github      :  @bmwachajr
Descrption  :  Allocate rooms to new Staff and Fellows at Andela

"""
class room(object):
    """A room at the dojo"""
    def __init__(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type

class livingSpace(room):
    """A living space at the dojo"""
    max_occupants = 4

    def __init__(self, room_name, room_type):
        super().__init__(room_name, room_type)
        self.occupants = []
