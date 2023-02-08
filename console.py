#!/usr/bin/python3
import cmd
import json
from models.base_model import BaseModel
from models import storage


def strip(s):
    return s.strip("'").strip('"')


class HBNBCommand(cmd.Cmd):
    """ Simple command processor for the hbnb project """

    prompt = "(hbnb) "
    intro = "A simple hbnb shell. Type help to list commands.\n"
    hbnb_classes = ["BaseModel"]

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
            new_base = BaseModel()
            new_base.save()
            print(new_base.id)

    def do_show(self, arg):
        """Print string representation of instance if it exists"""
        if not arg:
            print("** class name missing **")

        else:
            argv = arg.split(" ")
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing ** ")

                elif argc == 2:
                    storage.reload()
                    instance_key = f"BaseModel.{strip(argv[1])}"
                    base_model = storage.all().get(instance_key, None)

                    if base_model is None:
                        print("** no instance found ** ")
                    else:
                        print(BaseModel(**base_model))

    def do_destroy(self, arg):
        """Delete instance base on class name and id, save to json file"""
        if not arg:
            print("** class name missing **")

        else:
            argv = arg.split(" ")
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")

            else:
                if argc == 1:
                    print("** instance id missing ** ")

                elif argc == 2:
                    storage.reload()
                    instance_key = f"BaseModel.{strip(argv[1])}"
                    base_model = storage.all().get(instance_key, None)

                    if base_model is None:
                        print("** no instance found ** ")
                    else:
                        storage.all().pop(instance_key)
                        storage.save()

    def do_all(self, arg):
        """Print string representation of all instances"""
        storage.reload()
        if arg == "":
            print(json.dumps(
                [str(BaseModel(**v)) for k, v in storage.all().items()]))

        else:
            if arg not in self.hbnb_classes:
                print("** class doesn't exist **")
            else:
                print(json.dumps(
                    [str(BaseModel(**v)) for k, v in storage.all().items()]))

    def do_update(self, arg):
        """Update/Add instance attribute based on class, name and id"""

        if not arg:
            print("** class name missing **")

        else:
            argv = arg.split(" ")
            argc = len(argv)

            if argv[0] not in self.hbnb_classes:
                print("** class doesn't exist **")
                return

            if argc < 2:
                print("** instance id missing ** ")
                return

            else:
                storage.reload()
                instance_key = f"BaseModel.{strip(argv[1])}"
                base_model = storage.all().get(instance_key, None)

                if base_model is None:
                    print("** no instance found ** ")
                else:
                    if argc < 3:
                        print("** attribute name missing *")
                        return
                    if argc < 4:
                        print("** value missing **")
                        return
                    else:
                        base_model[argv[2]] = strip(argv[3])
                        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
