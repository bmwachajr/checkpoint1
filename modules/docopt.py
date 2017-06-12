"""
Usage:
  RoomMgt
  RoomMgt create_room <room_type> <room_name> ...

"""

import sys
import cmd
import docopt
from docopt import docopt
from dojo import dojo

dojo = dojo()

def docopt_cmd(func):
  """

  This decorator is used to simplify the try/except block and pass the result

  of the docopt parsing to the called action.

  """

  def fn(self, arg):
      try:
          opt = docopt(fn.__doc__, arg)

      except DocoptExit as e:
          print('Invalid Command!')
          print(e)
          return

      except SystemExit:
          return
      return func(self, opt)

  fn.__name__ = func.__name__
  fn.__doc__ = func.__doc__
  fn.__dict__.update(func.__dict__)
  return fn



class DojoCLI(cmd.Cmd):

  intro = 'Room Allocation System.' \
      + ' (type help for a list of commands.)'

  prompt = 'Dojo App '

  file = None

  @docopt_cmd
  def do_create_room(self, arg):
    """Usage:  create_room <room_type> <room_name> ..."""
    room_type = arg['<room_type>']
    room_list = arg['<room_name>']

    for room in room_list:
        new_room = dojo.create_room(room, room_type)
        if new_room != empty:
            print("A " + room_type + " called " + room + " has been successfully created! \n")

opt = docopt(__doc__, sys.argv[1:])
DojoCLI().cmdloop()
