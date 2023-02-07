#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime

"""
This module defines the BaseModel class which defines all common attr/methods
of other classes
"""


class BaseModel:
    """
    BaseModel Class

    __init__: Initializes BaseModel object/instance
    """

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """
        String representation of Base class

        Returns:
            String representation of Base class
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update attribute updated_at with current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Convert class object to dictionary

        Returns:
            Dictionary representation of class instance
        """
        # bm_dict ; base_model_dict
        bm_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        bm_dict["__class__"] = self.__class__.__name__

        # isoformat() == strftime("%Y-%m-%dT%H:%M:%S.%f")
        bm_dict["created_at"] = bm_dict["created_at"].isoformat()
        bm_dict["updated_at"] = bm_dict["updated_at"].isoformat()

        return bm_dict


if __name__ == "__main__":
    # Do stuff
    my_model = BaseModel()
    print(my_model.__str__())
    # my_model.name = "My First Model"
    # print(my_model)
    # print()
    # my_model.my_number = 89
    # print(my_model)
    # print()
    # my_model.save()
    # print(my_model)
    # my_model_json = my_model.to_dict()
    # print(my_model_json)
    # print("JSON of my_model:")
    # for key in my_model_json.keys():
    #     print(
    #         "\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key])
    #     )
