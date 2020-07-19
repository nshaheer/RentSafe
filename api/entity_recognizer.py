from abc import ABCMeta, abstractmethod


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        return 1
