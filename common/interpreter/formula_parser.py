import re

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        indent = "    " * level  # Indentation for each level
        print(f"{indent}{self.value}")
        for child in self.children:
            child.print_tree(level + 1)

    def to_json(self):
        if self.children:
            return {
                "type": "function",
                "value": self.value,
                "arguments": [child.to_json() for child in self.children]
            }
        else:
            return {
                "type": "literal",
                "value": self.value
            }
        
    def from_json(self, json_data):
        self.value = json_data.get('value')
        self.type = json_data.get('type')
        self.children = []

        arguments = json_data.get('arguments')
        if arguments:
            self.children = [Node().from_json(child) for child in arguments]

        return self

    def __str__(self):
        return str(self.to_json())


def parse_json_structure(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            # If value is a string and starts with '@', parse as a formula
            if isinstance(value, str) and value.startswith('@'):
                tree = parse_formula(value)
                json_data[key] = tree.to_json()
            else:
                # Recursively handle nested structures (dict or list)
                json_data[key] = parse_json_structure(value)
        return json_data
    elif isinstance(json_data, list):
        # Process each element in the list
        return [parse_json_structure(element) if not isinstance(element, str) or not element.startswith('@') 
                else parse_formula(element).to_json() for element in json_data]
    else:
        # Return the value as is if it's not a dict or list
        return json_data


def parse_formula(formula):
    # Regular expression to match a function call: @function_name(arguments)
    pattern = r"@(\w+)\("
    match = re.search(pattern, formula)
    
    if match:
        # Create a node for the function
        function_node = Node(match.group(1))
        
        # Find the corresponding closing parenthesis for the function arguments
        start_index = match.end()
        parentheses_count = 1
        end_index = start_index

        while end_index < len(formula) and parentheses_count > 0:
            if formula[end_index] == '(':
                parentheses_count += 1
            elif formula[end_index] == ')':
                parentheses_count -= 1
            end_index += 1

        # Extract arguments and recursively parse each one
        args_str = formula[start_index:end_index-1]
        args = []
        arg_start = 0
        for i, char in enumerate(args_str):
            if char == ',' and parentheses_count == 0:
                args.append(args_str[arg_start:i].strip())
                arg_start = i + 1
            elif char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
        args.append(args_str[arg_start:].strip())  # Add last argument

        for arg in args:
            if arg.startswith('@'):
                child_node = parse_formula(arg)
                function_node.add_child(child_node)
            else:
                function_node.add_child(Node(arg))
        return function_node
    else:
        return Node(formula)

