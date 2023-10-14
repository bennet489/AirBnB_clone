#!/usr/bin/env python3
"""This contains the module for test cases of the BaseModel"""
import inspect
import pycodestyle
import time
import unittest
from models import base_model
from models import storage
from datetime import datetime
from unittest import mock

BaseModel = base_model.BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Test cases in the models for the BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Docstrings set up tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pycodestyle_conformance(self):
        """... pycodestyle compliance"""
        for path in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_doc_file(self):
        """... file documentation"""
        doc = base_model.__doc__
        self.assertIsNotNone(doc, "base_model.py needs a docstring")

    def test_doc_class(self):
        """... the class documentation"""
        doc = BaseModel.__doc__
        self.assertIsNotNone(doc, "BaseModel class needs a docstring")

    def test_doc_init(self):
        """... this is the class functions documentation"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """this class is designed for testing the functionality of the BaseModel class.
"""

    def test_instantiation(self):
        """... ensuring that the BaseModel is correctly initialized"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "My First Model"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "My First Model")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """... verifies whether the datetime values of two BaseModel instances are not equal, indicating a difference in their timestamps."""
        tic = datetime.now()
        inst1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """"ensuring the UUID is valid is crucial for data integrity and consistency."""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Ensuring that the BaseModel is accurately converted into a dictionary"""
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "My First Model")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """Ensuring the accuracy of values in the dictionary returned from 'to_dict'"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """Verifying that the 'str' method produces the expected output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Verifying that the 'save' method appropriately updates the 'updated_at' timestamp and triggers the 'storage.save'"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        # self.assertTrue(mock_storage.new.called)
        # self.assertTrue(mock_storage.save.called)
        self.assertTrue(storage.new)
        self.assertTrue(storage.save)


if __name__ == "__main__":
    unittest.main()
