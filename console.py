#!/usr/bin/python3
"""
Module for main console
"""

import cmd
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines HBNBCommand class"""

    class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    prompt = "(hbnb) "

    def emptyline(self):
        """Handles empty lines"""
        return False

    def do_EOF(self, line):
        """EOF exits the program"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def _validate_class_and_id(self, args):
        """Helper method to validate class name and instance ID"""
        if len(args) == 0:
            print("** class name missing **")
            return False
        elif args[0] not in self.class_dict:
            print("** class doesn't exist **")
            return False
        elif len(args) < 2:
            print("** instance id missing **")
            return False
        return True

    def do_create(self, arg):
        """
        Creates a new instance of a class with given parameters.
        Usage: create <Class name> <param 1> <param 2> <param 3>...
        Param syntax: <key name>=<value>
        """
        args = arg.split()

        if len(args) < 1:
            print("Missing class name. Usage: create <Class name> <params>...")
            return

        class_name = args[0]
        if class_name not in self.class_dict:
            print(f"** {class_name} class doesn't exist **")
            return

        params = {}
        for param in args[1:]:
            # Split parameter into key and value using '='
            parts = param.split('=')
            if len(parts) == 2:
                key, value = parts
                # Check value type and format
                if value.startswith('"') and value.endswith('"'):
                    # String value
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    # Float value
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    # Integer value
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                params[key] = value

        new_instance = self.class_dict[class_name](**params)
        storage.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints string representation of an instance based on
        class name and ID
        Usage: $ show <class name> <id>"""
        args = arg.split()
        if not self._validate_class_and_id(args):
            return

        object_instances = storage.all()
        for full_key, instance in object_instances.items():
            key = full_key.split(".")
            if key[1] == args[1]:
                print("Found instance:")
                print(instance)
                return
        print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on class name and ID
        Usage: $ destroy <class name> <id>"""
        args = arg.split()
        if not self._validate_class_and_id(args):
            return

        object_instances = storage.all()
        for full_key in object_instances.keys():
            key = full_key.split(".")
            if key[1] == args[1]:
                del object_instances[full_key]
                storage.save()
                return
        print("** no instance found **")

    def do_all(self, arg):
        """Prints string representation of all class instances or
        instances of a specific class
        Usage: $ all [<class name>]"""
        args = arg.split()
        object_instances = storage.all()

        if len(args) == 0:
            for instance in object_instances.values():
                print(instance)

        elif len(args) == 1:
            if args[0] in self.class_dict:
                for key, instance in object_instances.items():
                    if instance.__class__.__name__ == args[0]:
                        print(instance)
                return
            else:
                print("** class doesn't exist **")
        else:
            print("Invalid usage of 'all' command")

    def do_update(self, arg):
        """Updates an instance based on class name and ID by adding/updating
        an attribute.
        Usage: $ update <class name> <id> <attribute name> <attribute value>"""
        args = arg.split()
        if not self._validate_class_and_id(args):
            return

        if len(args) < 4:
            print("** attribute name and/or value missing **")
            return

        class_name = args[0]
        instance_name = args[1]
        attribute_name = args[2]
        attribute_value = args[3]

        object_instances = storage.all()
        for full_key, instance in object_instances.items():
            key = full_key.split(".")
            if key[1] == instance_name:
                if hasattr(instance, attribute_name):
                    setattr(instance, attribute_name, attribute_value)
                    instance.updated_at = datetime.now()
                    storage.save()
                    return
        print("** no instance found **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
