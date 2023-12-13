import re
def regex(element, pattern, replacement, default_value):
    result = re.sub(pattern, replacement, element)
    if not result:
        return default_value
    else:
        return result