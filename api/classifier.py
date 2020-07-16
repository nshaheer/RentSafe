from abc import ABCMeta, abstractmethod


class ClassifierInterface(metaclass=ABCMeta):
    def classify(self, lease_id, paragraphs):
        pass


class DummyClassifier(ClassifierInterface):
    def classify(self, lease_id, paragraphs):
        return 1
