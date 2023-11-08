#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from os import getenv
from datetime import datetime
from typing import Dict

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        created_at = kwargs.get('created_at')
        updated_at = kwargs.get('updated_at')
        if created_at is None or not isinstance(created_at, datetime):
            created_at = datetime.now()
        if updated_at is None or not isinstance(updated_at, datetime):
            updated_at = datetime.now()
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self) -> str:
        cls = str(type(self).__name__)
        return f'[{cls}] ({self.id}) {self.__dict__}'

    def save(self) -> None:
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self) -> Dict:
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self) -> None:
        from models import storage
        storage.delete(self)
