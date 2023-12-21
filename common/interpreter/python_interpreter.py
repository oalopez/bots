import re
import importlib
import inspect

def interpret(function_call_string):
    # Regex to match 'module.function_name(arguments)'
    match = re.match(r"(\w+)\.(\w+)\((.*)\)", function_call_string)

    if match:
        module_name = match.group(1)
        function_name = match.group(2)
        arguments = match.group(3).split(',')
        return call_function(module_name, function_name, arguments)
    
    #TODO: Custom Exception
    raise Exception(f"Invalid function call string: {function_call_string}")

def call_function(module_name, function_name, arguments):
    
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise Exception(f"Error importing module: {str(e)}")

    # Get the function from the provided module or class
    func = getattr(module, function_name, None)

    if func:
        # Unpack arguments and pass them to the function
        try:
            result = func(*arguments)
        except TypeError as e:
            # Handle incorrect argument types or numbers
            result = f"Error: {str(e)}"
            #TODO: Custom exception
            raise Exception(result)
    else:
        # Handle the case where the function does not exist
        result = "Function not found"
        #TODO: Custom exception
        raise Exception(result)

    return result

# Example usage
# pre_process("math.sqrt(16)")
# pre_process("os.path.basename('/path/to/file.txt')")