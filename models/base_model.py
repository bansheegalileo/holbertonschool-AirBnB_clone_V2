#!/usr/bin/python3
"""Base class"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
import models

Base = declarative_base()


class BaseModel:
    """Base class for other classes to be used for the duration"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """__init__ method for BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        value = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid.uuid4()))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            models.storage.new(self)

    def save(self):
        """Update the updated_at attribute with new value and save to storage"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation of BaseModel class"""
        cp_dict = dict(self.__dict__)
        cp_dict['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in cp_dict:
            del cp_dict['_sa_instance_state']
        cp_dict['created_at'] = self.created_at.isoformat()
        cp_dict['updated_at'] = self.updated_at.isoformat()
        return cp_dict

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
