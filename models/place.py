#!/usr/bin/python3
"""
Place class module
"""


from typing import Any
from datetime import datetime
from models.base_model import BaseModel


class Place(BaseModel):
    """Defines Place class"""

    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""
    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    amenity_ids: str = ""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes instances"""
        if kwargs:
            if "__class__" in kwargs:
                del kwargs["__class__"]
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     self.timeformat)
            if "updated_at" in kwargs:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         self.timeformat)
            super().__init__(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
