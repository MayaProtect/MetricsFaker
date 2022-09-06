from uuid import UUID, uuid4
from mf_core.serializable import Serializable


class HiveEvent(Serializable):
    def __init__(self, event_type: str, event_timestamp: int, event_text: str, uuid: UUID = None):
        self.__uuid = uuid4() if uuid is None else uuid
        self.__event_type = event_type
        self.__event_timestamp = event_timestamp
        self.__event_text = event_text

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    @property
    def event_type(self) -> str:
        return self.__event_type

    @property
    def event_timestamp(self) -> int:
        return self.__event_timestamp

    @property
    def event_text(self) -> str:
        return self.__event_text

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "event_type": self.event_type,
            "event_timestamp": self.event_timestamp,
            "event_text": self.event_text
        }

    def __str__(self) -> str:
        return "Event: {} - {} - {}".format(self.event_type, self.event_timestamp, self.event_text)
