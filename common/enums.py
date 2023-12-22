from enum import Enum

class ExtractionType(Enum):
    JSON_ALL_RECORDS = "json-all-records"

class TransformationType(Enum):
    SIMPLE = "simple"
    REGEX = "regex"
    JSON_SOURCE = "json-source"
    CACHE="cache"

class OutputType(Enum):
    CSV = "csv"

class PaginationType(Enum):
    PARAMS = "params"

class TotalRecordsType(Enum):
    JSON = "json"

class StopSequenceType(Enum):
    PAGE_LIMIT = "page-limit"
    NO_MORE_RECORDS = "no-more-records"