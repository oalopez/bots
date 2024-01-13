from pyproj import Proj, transform, Transformer
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import transform as shapely_transform

from common.enums import GeometryFormat
from common.enums import CoordinateReference
from common.utils.exceptions import InvalidTypeException
import json

def geometry(geometry, source_format, target_format, source_crs=CoordinateReference.WGS84_4326.value, target_crs=CoordinateReference.WGS84_4326.value):
    if source_format != GeometryFormat.GEOJSON.value or target_format != GeometryFormat.WKT.value:
        raise InvalidTypeException("Unsupported format conversion: {} to {}".format(source_format, target_format))

    if source_crs != CoordinateReference.WGS84_4326.value:
        raise InvalidTypeException("Unsupported source CRS: " + source_crs)

    if target_crs != CoordinateReference.WGS84_4326.value:
        raise InvalidTypeException("Unsupported target CRS: " + target_crs)
    
    # If source and target formats are the same, no need to convert
    if source_format == target_format:
        return geometry

    if source_crs != target_crs:
        # Create a Transformer object for CRS transformation
        transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

        # Function to perform the CRS transformation
        def crs_transform(coord):
            return transformer.transform(*coord)

    # Convert GeoJSON to Shapely Geometry
    # geometry is str convert it to json
    geometry = json.loads(geometry)
    shapely_geom = shape(geometry)

    transformed_geom = shapely_geom
    if source_crs != target_crs:
        # Transform geometry to target CRS
        transformed_geom = shapely_transform(crs_transform, shapely_geom)

    # Convert to WKT format
    wkt_geometry = transformed_geom.wkt

    return wkt_geometry
