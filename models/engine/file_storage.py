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
    """what it says on the tin"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """returns dictionary"""
        if cls is not None:
            fs_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    fs_dict[key] = value
            return fs_dict
        return self.__objects

    def new(self, obj):
        """adds new to dict"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """saves dict to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp, f)

    def delete(self, obj=None):
        """delete obj from __objects"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.all():
                del self.all()[key]
                self.save()

    def reload(self):
        """loads dict"""
        from models import base_model, user, place, state, city, amenity, review

        classes = {
            'BaseModel': base_model.BaseModel,
            'User': user.User,
            'Place': place.Place,
            'State': state.State,
            'City': city.City,
            'Amenity': amenity.Amenity,
            'Review': review.Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
