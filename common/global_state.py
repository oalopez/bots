class GlobalState:
    def __init__(self):
        self._shared_data = {}

    def set_value(self, key, value):
        self._shared_data[key] = value

    def get_value(self, key):
        return self._shared_data.get(key)

    def reset(self):
        self._shared_data = {}


from enum import Enum
class GlobalStateKeys(Enum):
    CURRENT_BASE_DIR = "CURRENT_BASE_DIR"


global_state = GlobalState()