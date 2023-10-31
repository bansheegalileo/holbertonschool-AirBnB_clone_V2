#!/usr/bin/python3
"""
Base Model Module
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """BaseModel class that defines common attributes for other classes"""

    timeformat = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initializes BaseModel with attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        if kwargs:
            self.set_attributes_from_dict(kwargs)

        models.storage.new(self)

    def set_attributes_from_dict(self, attr_dict):
        """Sets object attributes from a dictionary"""
        for key, value in attr_dict.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the object"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.to_dict()
        )

    def save(self):
        """Updates the updated_at attribute and saves the instance"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing keys/values of __dict__
        of the instance"""
        nd = self.__dict__.copy()
        if "created_at" in nd and isinstance(nd["created_at"], datetime):
            nd["created_at"] = nd["created_at"].strftime(self.timeformat)
        if "updated_at" in nd and isinstance(nd["updated_at"], datetime):
            nd["updated_at"] = nd["updated_at"].strftime(self.timeformat)
        nd["__class__"] = self.__class__.__name__
        return nd
