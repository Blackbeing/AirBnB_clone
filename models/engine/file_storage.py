#!/usr/bin/python3
import json
from pathlib import Path

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects
    
    def new(self, obj):
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as fd:
            json.dump(FileStorage.__objects, fd)

    def reload(self):
        if Path(FileStorage.__file_path).exists():
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as fd:
                FileStorage.__objects = json.load(fd)

if __name__ == "__main__":
    x = FileStorage()
    print(x.all())

