from uuid import UUID
from mf_core.hive_event import HiveEvent


class HiveEventCollection(list):
    def __init__(self):
        super().__init__()
        self.__last_collect_timestamp = 0

    def create_event(self, event_type: str, event_timestamp: int, event_text: str) -> UUID:
        """
        Creates a new hive and returns its uuid.
        :param event_type:
        :param event_timestamp:
        :param event_text:
        :return:
        """
        hive_event = HiveEvent(event_type, event_timestamp, event_text)
        uuid = hive_event.uuid
        self.append(hive_event)
        return uuid

    def get_by_uuid(self, uuid):
        """
        Returns the hive event with the given uuid.
        :param uuid:
        :return:
        """
        for hive_event in self:
            if hive_event.uuid == uuid:
                return hive_event
        return None

    def to_array(self):
        """
        Returns the hive events in an array.
        :return:
        """
        events_array = []
        for hive_event in self:
            events_array.append(hive_event.to_dict())