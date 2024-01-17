from common.enums import OutputType
from common.utils.exceptions import InvalidTypeException
from common.utils.profiling import lap_time


@lap_time(tolerance=2)
def output(transformed_df, output_json, output_id=None, caches=None):

    output_type = output_json['output']['type']
    
    if output_type == OutputType.CSV.value:
        from output.type.csv import generate_output
        return generate_output(transformed_df, output_json, output_id, caches)
    else:
        raise InvalidTypeException("Output type: " + output_type + " is not supported")