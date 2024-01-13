from common.enums import OutputType
from common.utils.exceptions import InvalidTypeException
from common.utils.profiling import lap_time

@lap_time(tolerance=2)
def generate_output(base_directory, output_json, transformed_df, context_vars, output_id=None):
    output_type = output_json['output']['type']
    
    if output_type == OutputType.CSV.value:
        from output.type.csv import generate_output
        return generate_output(base_directory, output_json, transformed_df, context_vars, output_id)
    else:
        raise InvalidTypeException("Output type: " + output_type + " is not supported")