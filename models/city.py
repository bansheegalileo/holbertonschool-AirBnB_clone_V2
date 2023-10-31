#!/usr/bin/python3

"""Defines the City class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """Represents a City."""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), nullable=False)

    places = relationship("Place", backref="cities", cascade="all, delete-orphan")
