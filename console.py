#!/usr/bin/python3
import cmd
import json
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def strip(s):
    return s.strip("'").strip('"')


class HBNBCommand(cmd.Cmd):
    """Simple command processor for the hbnb project"""

    prompt = "(hbnb) "
    intro = "A simple hbnb shell. Type help to list commands.\n"
    hbnb_classes = [
            "BaseModel", "User", "State", "City",
            "Amenity", "Place", "Review"
    ]

    def do_EOF(self, arg):
        """Exit"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def postloop(self):
        print()

    def do_create(self, arg):
        """Create new instance of BaseModel, save to json file and print id"""
        if not arg:
            print("** class name missing **")

        elif arg not in self.hbnb_classes:
            print("** class doesn't exist **")

        else:
            eval_string = f"{arg}()"
            new_base = eval(eval_string)
            new_base.save()
            print(new_base.id)

    def do_show(self, arg):
        """Print string representation of instance if it exists"""
        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing ** ")

                elif argc == 2:
                    storage.reload()
                    instance_key = f"{argv[0]}.{strip(argv[1])}"
                    instance_dict = storage.all().get(instance_key, None)

                    if instance_dict is None:
                        print("** no instance found ** ")
                    else:
                        eval_string = f"{argv[0]}(**instance_dict)"
                        print(eval(eval_string))

    def do_destroy(self, arg):
        """Delete instance base on class name and id, save to json file"""
        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing ** ")

                elif argc == 2:
                    storage.reload()
                    instance_key = f"{argv[0]}.{strip(argv[1])}"
                    instance_dict = storage.all().get(instance_key, None)

                    if instance_dict is None:
                        print("** no instance found ** ")
                    else:
                        storage.all().pop(instance_key)
                        storage.save()

    def do_all(self, arg):
        """Print string representation of all instances"""

        def eval_str(string):
            return string.split(".")[0]

        storage.reload()

        if arg == "":
            print(
                json.dumps(
                    [str(eval(f"{eval_str(k)}(**v)"))
                     for k, v in storage.all().items()]
                )
            )

        else:
            if arg not in self.hbnb_classes:
                print("** class doesn't exist **")
            else:
                print(
                    json.dumps(
                        [
                            str(eval(f"{arg}(**v)"))
                            for k, v in storage.all().items()
                            if arg == v["__class__"]
                        ]
                    )
                )

    def do_update(self, arg):
        """Update/Add instance attribute based on class, name and id"""

        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")
                return

            if argc < 2:
                print("** instance id missing ** ")
                return

            else:
                storage.reload()
                instance_key = f"{argv[0]}.{strip(argv[1])}"
                instance_dict = storage.all().get(instance_key, None)

                if instance_dict is None:
                    print("** no instance found ** ")
                else:
                    if argc < 3:
                        print("** attribute name missing *")
                        return
                    if argc < 4:
                        print("** value missing **")
                        return
                    else:
                        instance_dict[argv[2]] = strip(argv[3])
                        storage.save()

    def do_count(self, arg):
        """Count number of instances of a class """

        if not arg:
            print("** class name missing **")

        else:
            argv = shlex.split(arg)
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")
            else:
                storage.reload()
                count = [v for v in storage.all().values()
                         if arg == v["__class__"]]
                print(len(count))

    def default(self, arg):
        """Parse unrecognized command prefixes"""

        # parseline returns tuple (command, args, line)
        command, args, line = cmd.Cmd.parseline(self, arg)
        # ex. arg = User.all()
        # command, args, line = ("User", ".all()",  "User.all()")
        # args = args.replace(".", "").replace("(", "").replace(")", "")
        if command in self.hbnb_classes:

            do_cmd, _, add_args = args.strip(".)").partition("(")

            # Convert args to a list and join with spaces
            add_args = " ".join(add_args.split(","))

            if add_args == "":
                new_arg = f"{do_cmd} {command}"
            else:
                new_arg = f"{do_cmd} {command} {add_args}"

            cmd.Cmd.onecmd(self, new_arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
