"""
Usage:
  Dojo
  Dojo create_room <room_type> <room_name> ...
  Dojo add_person <person_name> <FELLOW_or_STAFF> [<wants_accomodation>]
  Dojo print_room <room_name>
  Dojo load_people
  Dojo print_person <first_name> <last_name>
  Dojo reallocate_person <person name>
  Dojo print_allocations [<-o=filename>]
  Dojo print_unallocated [<-o=filename>]
  Dojo save_state ['<-o=sqlite_database>']
  Dojo load_state ['<-o=sqlite_database>']

"""
import cmd
from docopt import docopt, DocoptExit
from functools import wraps
import sys
from dojo import dojo

dojo = dojo()


def docopt_cmd(func):  # pragma: no cover
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    @wraps(func)
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)

    return fn


class DojoCLI(cmd.Cmd):
    intro = 'Welcome to Dojo Command Line Interface' \
        + ' (type help for a list of commands.)'
    prompt = 'Dojo '

    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage:  create_room <room_type> <room_name> ..."""
        room_type = arg['<room_type>']
        room_list = arg['<room_name>']

        # create rooms
        for room in room_list:
            output = dojo.create_room(room, room_type)
            print(output)
        print("")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage:  add_person <first_name> <last_name> <person_type> [<wants_accomodation>]"""
        person_name = arg['<first_name>'] + " " + arg['<last_name>']
        person_type = arg['<person_type>']
        wants_accomodation = arg['<wants_accomodation>']

        # add the person
        output = dojo.add_person(person_name, person_type, wants_accomodation)
        print(output)

    @docopt_cmd
    def do_print_person(self, arg):
        """Usage: print_person <first_name> <last_name> """
        person_name = arg['<first_name>'] + " " + arg['<last_name>']

        output = dojo.find_person(person_name)

        if output is not None:
            print("Name: " + output.person_name)
            print("Type: " + output.person_type)
            print("Office Space: " + output.officeSpace)
            if output.person_type == "fellow":
                if output.livingSpace is not None:
                    print("Living space: " + output.livingSpace)
        else:
            print("Person Not Found. Please try again")
        print("")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name> """
        person_name = arg['<first_name>'] + " " + arg['<last_name>']
        new_room = arg['<new_room_name>']

        #reallocate person
        output = dojo.reallocate_person(person_name, new_room)
        if isinstance(output, str):
            print(output)
        else:
            print(output.person_name + " was successfully reallocated to " + new_room)
            print("")

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people """
        output = dojo.load_people('file.txt')

        #print details
        if output == None:
            print('Nothing was loaded')
        else:
            for person in output:
                print(person)
                print("")

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [<-o=filename>]"""
        if arg['<-o=filename>'] != None and arg['<-o=filename>'] != "":
            output = dojo.print_allocations(arg['<-o=filename>'])

        #print information
        if len(dojo.all_rooms) == 0:
            print("No rooms and allocations added yet")
        else:
            for room in dojo.all_rooms:
                print(room.room_name + " - " + room.room_type)
                print("........................................")
                for person in room.occupants:
                    print(person)
                print("")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [<-o=filename>]"""
        if arg['<-o=filename>'] != None and arg['<-o=filename>'] != "":
            output = dojo.print_unallocated(arg['<-o=filename>'])

        #print information
        if len(dojo.unallocated_offices) == 0:
            print("No people with office space unallocations")
        else:
            print("Employees unallocated Office spaces \n" + "........................................")
            for person in dojo.unallocated_offices:
                print(person.person_name + " (" +(person.person_type) + ")")
        print("")

        #print information
        if len(dojo.unallocated_livingspaces) == 0:
            print("No people with Living space unallocations")
        else:
            print("Employees unallocated Living spaces\n" + "........................................")
            for person in dojo.unallocated_livingspaces:
                print(person.person_name + " (" +(person.person_type) + ")")
        print("")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room = dojo.find_room(arg['<room_name>'])

        if room == None:
            print("Room not found, please try again")
        else:
            print(room.room_name + " " + room.room_type)
            print("......................................")
            for person in room.occupants:
                print(person.person_name + " (" + person.person_type + ")")

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [<--db=sqlite_database>]"""
        if arg['<--db=sqlite_database>'] == None:
            arg['<--db=sqlite_database>'] = "database.db"
        output = dojo.save_state(arg['<--db=sqlite_database>'])
        if output == True:
            print("successfully saved state to database")
        else:
            print("There was a problem in saving state.")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [<--db=sqlite_database>]"""
        if arg['<--db=sqlite_database>'] is None:
            database_name = "database.db"
        else:
            database_name = arg['<--db=sqlite_database>']

        dojo.load_state(database_name)

        if dojo is not None:
            print("We have lift off")

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


if __name__ == '__main__':
    opt = docopt(__doc__, sys.argv[1:])
    DojoCLI().cmdloop()
