from __future__ import annotations
from uuid import UUID, uuid4
from random import randint
from mf_core.serializable import Serializable


class Owner(Serializable):
    def __init__(self, uuid: UUID = None, firstname: str = None, lastname: str = None, email: str = None):
        self.__uuid = uuid4() if uuid is None else uuid
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    @property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, value: str) -> None:
        self.__firstname = value

    @property
    def lastname(self) -> str:
        return self.__lastname

    @lastname.setter
    def lastname(self, value: str) -> None:
        self.__lastname = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value

    @property
    def fullname(self) -> str:
        return "{} {}".format(self.firstname, self.lastname)

    def __str__(self) -> str:
        return self.fullname

    @staticmethod
    def generate_fake() -> Owner:
        """
        Generate a fake owner
        :return: Owner generated
        """
        list_fake_firstname = ["Claire", "Peter", "Samir", "Jill", "Joe", "Souhaïb", "Marc", "Marcel", "Miguel", "Michel"]
        list_fake_lastname = ["Doe", "Durant", "Dupuis", "Ponche", "Rodriguez", "Delacour", "Smith", "Dutronc",
                              "Dutilleul", "Dupont"]
        list_fake_email = ["example@gmail.com", "example@hotmail.com", "example@yahoo.com", "example@outlook.com",
                           "example@live.com", "example@orange.fr"]

        return Owner(uuid4(), list_fake_firstname[randint(0, len(list_fake_firstname) - 1)],
                     list_fake_lastname[randint(0, len(list_fake_lastname) - 1)],
                     list_fake_email[randint(0, len(list_fake_email) - 1)])

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }
