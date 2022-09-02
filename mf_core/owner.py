from uuid import UUID, uuid4


class Owner:
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
