from pyproj import Proj, transform, Transformer
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import transform as shapely_transform
import logging

from common.enums import GeometryFormat
from common.enums import CoordinateReference
from common.utils.exceptions import InvalidTypeException
from common.interpreter.formula_executor import execute_node


logger = logging.getLogger(__name__)

def geometry(geometry, element, source_format, target_format, source_crs=CoordinateReference.WGS84_4326.value, target_crs=CoordinateReference.WGS84_4326.value):
    if source_format != GeometryFormat.GEOJSON.value or target_format != GeometryFormat.WKT.value:
        raise InvalidTypeException("Unsupported format conversion: {} to {}".format(source_format, target_format))

    if source_crs != CoordinateReference.WGS84_4326.value:
        raise InvalidTypeException("Unsupported source CRS: " + source_crs)

    if target_crs != CoordinateReference.WGS84_4326.value:
        raise InvalidTypeException("Unsupported target CRS: " + target_crs)
    
    geometry = execute_node(geometry, element)

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
    if geometry is not None:
        shapely_geom = shape(geometry)
    else:
        # create an empty polygon
        logger.warn('Empty geometry. Element: ' + str(element))
        shapely_geom = Polygon()

    transformed_geom = shapely_geom
    if source_crs != target_crs:
        # Transform geometry to target CRS
        transformed_geom = shapely_transform(crs_transform, shapely_geom)

    # Convert to WKT format
    wkt_geometry = transformed_geom.wkt

    return wkt_geometry
