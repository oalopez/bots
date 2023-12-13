from enum import Enum

class ExtractionType(Enum):
    JSON_ALL_RECORDS = "json-all-records"

class TransformationType(Enum):
    SIMPLE = "simple"
    REGEX = "regex"
    JSON_SOURCE = "json-source"

class LoaderType(Enum):
    pass