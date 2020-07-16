from abc import ABCMeta, abstractmethod


class StorageInterface(metaclass=ABCMeta):
    def add_lease(self, id, paragraphs, **kwargs):
        pass


class MemStorage(StorageInterface):
    def __init__(self):
        self.storage = {}

    def add_lease(self, id, paragraphs, **kwargs):
        lease = {
            "paragraphs": paragraphs,
        }
        lease.update(kwargs)

        self.storage[id] = lease
