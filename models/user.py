#!/usr/bin/python3

""" Module that writes subclass User """
from models.base_model import BaseModel


class User(BaseModel):
    """ User class is a subclass of BaseModel """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
