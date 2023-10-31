#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import BaseModel

class City(BaseModel):
    """Represents a City."""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a new City instance."""
        super().__init__(*args, **kwargs)
