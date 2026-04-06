"""The module contains implementation of game subsystem class"""


class SubSystem:
    game = None
    subsystem_name: str = None

    @classmethod
    def on_subsystem_init(cls):
        pass

    @classmethod
    def init_subsystem(cls, game_obj):
        cls.game = game_obj
        if cls.subsystem_name:
            setattr(game_obj, cls.subsystem_name, cls())
        cls.on_subsystem_init()
