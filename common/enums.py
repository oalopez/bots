from enum import Enum

class ExtractionType(Enum):
    JSON_ALL_RECORDS = "json-all-records"
    INPUT_JSON_X_PAGE = "input-json-per-page"

class TransformationType(Enum):
    SIMPLE = "simple"
    REGEX = "regex"
    JSON_SOURCE = "json-source"
    CACHE="cache"
    GEOMETRY="geometry"

class OutputType(Enum):
    CSV = "csv"

class PaginationType(Enum):
    PARAMS = "params"

class TotalRecordsType(Enum):
    JSON = "json"
    TOTAL_INPUT = "total-input"

class StopSequenceType(Enum):
    PAGE_LIMIT = "page-limit"
    NO_MORE_RECORDS = "no-more-records"

class CacheSourceType(Enum):
    JSON = "json"
    CSV = "csv"

class GeometryFormat(Enum):
    WKT = "wkt"
    GEOJSON = "geojson"


class CoordinateReference(Enum):
    WGS84_4326 = "EPSG:4326"
    WEB_MERCATOR_3857  = "EPSG:3857"

class JsonErrorActionType(Enum):
    SKIP = "skip"
    STOP = "stop"

class OutputTransformationType(Enum):
    CAST="cast"
    TRUNCATE="truncate"

class InputType(Enum):
    CSV="csv"