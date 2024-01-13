from enum import Enum

class ExtractionType(Enum):
    JSON_ALL_RECORDS = "json-all-records"

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