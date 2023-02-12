#!/usr/bin/python3
import json
from pathlib import Path


ALL_CLASSES = ["BaseModel", "User", "State",
               "City", "Amenity", "Place", "Review"]


class BaseModelEncoder(json.JSONEncoder):
    """
    Serialize instances of BaseModel to dictionary

    Returns:
        dictionary if obj is instance of BaseModel, else default object
    """
    def default(self, obj):
        if obj.__class__.__name__ in ALL_CLASSES:
            return obj.to_dict()
        return super().default(self, obj)


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
                FileStorage.__objects = json.load(fd)
