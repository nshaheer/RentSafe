from abc import ABCMeta, abstractmethod


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, lease_id, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, lease_id, paragraphs):
        return 1
