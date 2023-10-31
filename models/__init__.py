#!/usr/bin/python3
"""
Module creates a unique storage instance for your application
"""
import os

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
