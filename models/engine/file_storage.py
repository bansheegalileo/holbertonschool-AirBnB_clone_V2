#!/usr/bin/python3
import json
import os
from typing import Dict, Type
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    def __init__(self):
        self.file_path = "./file.json"
        self.objects = {}

    def clear(self):
        self.objects = {}

    def all(self, cls=None) -> Dict[str, object]:
        if cls is not None:
            return {key: obj for key, obj in self.objects.items()
                    if isinstance(obj, cls)}
        return self.objects

    def new(self, obj: object):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.objects[key] = obj

    def save(self):
        nd = {key: value.to_dict() for key, value in self.objects.items()}
        with open(self.file_path, "w") as f:
            json.dump(nd, f)

    def reload(self):
        try:
            with open(self.file_path, "r", encoding="UTF-8") as f:
                reloaded = json.load(f)
                for obj_id, obj_data in reloaded.items():
                    class_name = obj_data.get("__class__")
                    cls_func = self.get_class(class_name)
                    if cls_func:
                        obj = cls_func(**obj_data)
                        self.objects[obj_id] = obj
        except FileNotFoundError:
            # Handle the case when the file doesn't exist
            pass
        except Exception as e:
            # Handle other exceptions, such as JSON decoding errors
            print(f"Error while reloading data: {e}")

    def delete(self, obj=None):
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.objects:
                del self.objects[key]

    @staticmethod
    def get_class(class_name: str) -> Type[object] or None:
        # Define mappings from class names to class objects
        class_mappings = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
        return class_mappings.get(class_name, None)
