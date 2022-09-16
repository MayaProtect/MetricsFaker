from abc import abstractmethod


class Serializable:
    @abstractmethod
    def to_dict(self) -> dict:
        pass
