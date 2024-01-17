import unittest
from common.interpreter.formula_parser import parse_formula
from common.interpreter.formula_executor import execute_node

class TestExecuteNode(unittest.TestCase):

    def test_jsonpath_objectid(self):
        # Provided JSON data
        json_data = {
            "properties": {
                "objectid": 2001,
                "exclusiones": "Ley_2a",
                "st_area(shape)": 160514.34854422501,
                "st_length(shape)": 2576.0087884864488
            }
        }
        
        # Use parse_formula to create the node structure
        formula = "@jsonpath($.properties.objectid)"
        root = parse_formula(formula)
        
        # Execute the node
        result = execute_node(base_directory='', node=root, json_data=json_data)

        # Check the result
        self.assertEqual(result, 2001)

    def test_custom_function(self):
        # Provided JSON data
        json_data = {
            "properties": {
                "objectid": 2001,
                "exclusiones": "Ley_2a",
                "st_area(shape)": 160514.34854422501,
                "st_length(shape)": 2576.0087884864488
            }
        }
        
        # Use parse_formula to create the node structure
        formula = "@roundup(@jsonpath($.properties['st_area(shape)']),4)"
        root = parse_formula(formula)
        
        # Execute the node
        result = execute_node(base_directory='/Volumes/External/ext-vscode-workspaces/bots/tests', node=root, json_data=json_data)

        # Check the result
        self.assertEqual(result, 160514.3485)

if __name__ == '__main__':
    unittest.main()
