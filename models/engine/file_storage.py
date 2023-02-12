#!/usr/bin/python3
import json
from pathlib import Path

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class BaseModelEncoder(json.JSONEncoder):
    """
    Serialize instances of BaseModel to dictionary

    Returns:
        dictionary if obj is instance of BaseModel, else default object
    """
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.to_dict()
        return super().default(self, obj)


def base_model_object_hook(dct):
    """
    Function that will be called with the result of any object literal decoded

    Returns:
        BaseModel instance or default object
    """

    if "__class__" in dct:
        return eval(f"{dct['__class__']}(**dct)")
    return dct


class FileStorage:
    """
    Serialize BaseModel instances to JSON file and vice versa
    """
    __file_path = "file.json"
    __objects = {}

    def __init__(self, file_path=None):
        if file_path is not None:
            FileStorage.__file_path = file_path

    def all(self):
        """
        Get all object instances
        Returns:
            All object instances
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Create a new object instance
        """
        FileStorage.__objects[
                f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serialize objects (__objects) to JSON file
        """
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as fd:
            json.dump(FileStorage.__objects, fd, cls=BaseModelEncoder)

    def reload(self):
        """
        De-serialize object from JSON file and store in __objects
        """
        if Path(FileStorage.__file_path).exists():
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as fd:
                FileStorage.__objects = json.load(
                        fd, object_hook=base_model_object_hook)
