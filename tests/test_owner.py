import unittest
from mf_core import Owner
from uuid import uuid4


class TestOwner(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.__owner = Owner()

    def test_create_owner(self):
        self.assertTrue(type(self.__owner) == Owner)
        self.assertEqual(self.__owner.firstname, None)
        self.assertEqual(self.__owner.lastname, None)
        self.assertEqual(self.__owner.email, None)

    def test_create_owner_with_uuid(self):
        uuid = uuid4()
        owner = Owner(uuid)
        self.assertTrue(owner.uuid == uuid)

    def test_owner_set_firstname(self):
        self.__owner.firstname = "John"
        self.assertEqual(self.__owner.firstname, "John")

    def test_owner_set_lastname(self):
        self.__owner.lastname = "Doe"
        self.assertEqual(self.__owner.lastname, "Doe")

    def test_owner_set_email(self):
        self.__owner.email = "test@test.com"
        self.assertEqual(self.__owner.email, "test@test.com")

    def test_owner_get_fullname(self):
        self.__owner.firstname = "John"
        self.__owner.lastname = "Doe"
        self.assertEqual(self.__owner.fullname, "John Doe")

    def test_owner_get_uuid(self):
        uuid = uuid4()
        owner = Owner(uuid)
        self.assertTrue(owner.uuid == uuid)

    def test_owner_str(self):
        self.__owner.firstname = "John"
        self.__owner.lastname = "Doe"
        self.assertEqual(str(self.__owner), "John Doe")

    def test_owner_generate_fake(self):
        owner = Owner.generate_fake()
        self.assertTrue(type(owner) == Owner)
        self.assertTrue(owner.firstname is not None)
        self.assertTrue(owner.lastname is not None)
        self.assertTrue(owner.email is not None)
