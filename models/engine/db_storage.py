#!/usr/bin/python3
"""New DBstorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity

class DBStorage:
    _engine = None
    _session = None

    def __init__(self):
        self._initialize_database()

    def _initialize_database(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        try:
            self._engine = create_engine(f"mysql+mysqldb://{user}:{passwd}@{host}/{database}", pool_pre_ping=True)
            if env == "test":
                Base.metadata.drop_all(self._engine)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self._engine = None

    def all(self, cls=None):
        if cls:
            if isinstance(cls, str):
                cls = self._get_class_by_name(cls)
            return {f"{instance.__class__.__name__}.{instance.id}": instance for instance in self._session.query(cls).all()}

        all_objects = {}
        for obj_class in [City, State, User, Place, Review, Amenity]:
            all_objects.update({f"{instance.__class__.__name__}.{instance.id}": instance for instance in self._session.query(obj_class).all()})

        return all_objects

    def new(self, obj):
        self._session.add(obj)

    def save(self):
        self._session.commit()

    def delete(self, obj=None):
        if obj:
            self._session.delete(obj)

    def reload(self):
        if self._engine:
            Base.metadata.create_all(self._engine)
            session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
            self._session = scoped_session(session_factory)

    def _get_class_by_name(self, class_name):
        class_mapping = {
            "City": City,
            "State": State,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity,
        }
        return class_mapping.get(class_name)
