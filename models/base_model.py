#!/usr/bin/python3
"""Base Model Module"""

import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer

Base = declarative_base()

class BaseModel:
    """BaseModel class that defines common attributes for other classes"""

    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes BaseModel with attributes"""
        self.id = str(uuid.uuid4())
        if kwargs:
            self.set_attributes_from_dict(kwargs)
        models.storage.new(self)

    def set_attributes_from_dict(self, attr_dict):
        """Sets object attributes from a dictionary"""
        for key, value in attr_dict.items():
            if key != "__class__":
                setattr(self, key, value)

    def save(self):
        """Updates the updated_at attribute and saves the instance"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Returns a dict. containing keys/values of __dict__ of the instance"""
        nd = self.__dict__.copy()
        if "_sa_instance_state" in nd:
            del nd["_sa_instance_state"]
        if "created_at" in nd and isinstance(nd["created_at"], datetime):
            nd["created_at"] = nd["created_at"].isoformat()
        if "updated_at" in nd and isinstance(nd["updated_at"], datetime):
            nd["updated_at"] = nd["updated_at"].isoformat()
        nd["__class__"] = self.__class__.__name
        return nd

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
