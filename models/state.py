#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models

class State(BaseModel, Base):
    """
    state class
    """

    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        name = ""

    @property
    def cities(self) -> "list[City]":
        """
        gets linked cities
        """
        state_id = self.id
        cities = []
        for city in models.storage.all(City).values():
            if city.state_id == state_id:
                cities.append(city)
        return cities
