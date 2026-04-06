"""The module contains base entity class"""

from NarratorEngine.subsystem import SubSystem


class Entity(SubSystem):

    def __init__(self):
        self.create_entity()

    def create_entity(self):
        pass

    def save_base_data(self):
        return str(self.__class__.__name__)

    def load_base_data(self):
        pass

    def save_extra_data(self):
        pass

    def load_extra_data(self):
        pass
