#!/usr/bin/python3
import unittest
from pathlib import Path
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    # @classmethod
    def setUp(self):
        self.storage = FileStorage()
        self.base = BaseModel()

    # @classmethod
    def tearDown(self):
        del self.storage
        del self.base
        # Path("file.json").unlink()

    def test_new(self):
        self.storage.new(self.base)
        self.assertIn(self.base.to_dict(),
                      [v for k, v in self.storage.all().items()])

    def test_all(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_save(self):
        self.storage.save()
        self.storage.reload()
        self.assertIn(self.base.to_dict(),
                      [v for k, v in self.storage.all().items()])

    def test_reload(self):
        self.storage.reload()
        self.assertTrue(self.storage.all() != {})


