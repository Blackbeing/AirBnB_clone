#!/usr/bin/python3

import unittest
from io import StringIO
from unittest import mock
from console import HBNBCommand


class TestCMD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actions = [
            action.partition("_")[2]
            for action in dir(HBNBCommand())
            if action.startswith("do_")
        ]

    def setUp(self):
        self.cmd = HBNBCommand()

    def teardown(self):
        self.cmd.onecmd("quit")

    def test_print_help(self):
        for action in self.actions:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"help {action}")
                self.assertEqual(
                    f.getvalue().strip(),
                    eval(f"self.cmd.do_{action}.__doc__.strip()"),
                )

    def test_prompt(self):
        self.assertEqual(self.cmd.prompt, "(hbnb) ")

    def test_class_name_missing(self):
        for action in ["create", "show", "update", "destroy", "count"]:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{action}")
                self.assertEqual(
                    f.getvalue().strip(), "** class name missing **"
                )

    def test_class_doest_exist(self):
        for action in ["create", "show", "update", "destroy", "count"]:
            with mock.patch("sys.stdout", new=StringIO()) as f:
                self.cmd.onecmd(f"{action} MyModel")
                self.assertEqual(
                    f.getvalue().strip(), "** class doesn't exist **"
                )

    def test_class_id_missing(self):
        for action in ["show", "update", "destroy"]:
            for klass in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review",
            ]:
                with mock.patch("sys.stdout", new=StringIO()) as f:
                    self.cmd.onecmd(f"{action} {klass}")
                    self.assertEqual(
                        f.getvalue().strip(), "** instance id missing **"
                    )
