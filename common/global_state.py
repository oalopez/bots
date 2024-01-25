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
    INPUT_RECORDS = "INPUT_RECORDS"
    CURRENT_INPUT_PART = "CURRENT_INPUT_PART" # could be a page or a row depending on the input type
    TOTAL_RECORDS = "TOTAL_RECORDS"


global_state = GlobalState()