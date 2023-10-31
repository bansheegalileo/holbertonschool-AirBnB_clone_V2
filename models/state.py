#!/usr/bin/python3
""" Module that writes the subclass State """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ The State Class is a subclass of BaseModel """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if models.storage_type == "db":
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            city_list = []
            for city in list(models.storage.all("City").values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
