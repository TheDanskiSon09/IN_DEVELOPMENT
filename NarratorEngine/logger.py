"""The module contains impementation of base logger class"""

from NarratorEngine.subsystem import SubSystem


class Logger(SubSystem):
    from NarratorEngine.constants import TXT_COLOR_DEFAULT, TXT_COLOR_YELLOW, TXT_COLOR_RED

    message_types_map = {
        'NOTE': TXT_COLOR_DEFAULT,
        'WARNING': TXT_COLOR_YELLOW,
        'ERROR': TXT_COLOR_RED
    }

    def __init__(
            self
    ) -> None:
        pass

    def log(
            self,
            message: str,
            message_type: str = None
    ) -> str:
        from datetime import datetime
        message_color = None
        try:
            message_color = self.message_types_map[message_type]
        except KeyError:
            message_type = 'NOTE'
            message_color = self.message_types_map[message_type]
        print(f'[{datetime.now()}] {message_type}: {message}')
        #print(f'[{datetime.now()}]')
        #if message_type:
        #print(self.message_types_map[message_type])
        #else:
        #print(self.message_types_map['NOTE'])
