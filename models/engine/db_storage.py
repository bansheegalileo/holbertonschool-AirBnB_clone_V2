#!/usr/bin/python3
"""
model to mange DB storage using sqlAlchemy
"""


import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


class DBStorage:
    """
        This class manage DB storage for AirBnb
        Clone using sqlAlchemy
    """
    __engine = None
    __session = None
    all_classes = ["State", "City", "User", "Place", "Review"]

    def __init__(self):
        """
            Init __engine based on the Enviroment
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        exec_db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HBNB_MYSQL_USER,
                                            HBNB_MYSQL_PWD,
                                            HBNB_MYSQL_HOST,
                                            HBNB_MYSQL_DB
                                                )
        self.__engine = create_engine(exec_db, pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current database session for objects of the given class.

        If cls is None, queries all types of objects.

        Returns:
            A dictionary of queried classes in the format <class name>.<obj id> = obj.
        """
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = self.get_class(cls)
            objects = {f"{type(obj).__name__}.{obj.id}": obj for obj in self.__session.query(cls).all()}
        else:
            for class_name, class_ in self.get_supported_classes().items():
                objects.update({f"{class_name}.{obj.id}": obj for obj in self.__session.query(class_).all()})
        return objects

    def get_supported_classes(self):
        """Get a dictionary of supported classes and their corresponding names."""
        return {class_.__name__: class_ for class_ in Base._decl_class_registry.values() if hasattr(class_, '__tablename__')}

    def get_class(self, class_name):
        """Get the class based on the provided class name."""
        supported_classes = self.get_supported_classes()
        return supported_classes.get(class_name)

    def new(self, obj):
        """
            Creating new instance in db storage
        """
        self.__session.add(obj)

    def save(self):
        """
            save to the db storage
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete obj from db storage
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
            create table in database
        """
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self):
        """
            Closing the session
        """
        self.reload()
        self.__session.close()