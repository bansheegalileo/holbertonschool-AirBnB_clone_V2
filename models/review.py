#!/usr/bin/python3

""" Module that writes the subclass Review"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class is a subclass of basemodel
    """
    place_id = ""
    user_id = ""
    test = ""
