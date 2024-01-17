import unittest
from common.interpreter.formula_parser import parse_formula

# [Include the Node class and parse_formula function here]

class TestParseFormula(unittest.TestCase):
    def check_structure(self, node, expected_name, expected_children_names):
        self.assertEqual(node.name, expected_name)
        self.assertEqual(len(node.children), len(expected_children_names))
        for child, expected_name in zip(node.children, expected_children_names):
            if isinstance(expected_name, tuple):
                # If the expected name is a tuple, it's a function with arguments
                self.check_structure(child, *expected_name)
            else:
                # Otherwise, it's a single argument
                self.assertEqual(child.name, expected_name)

    def test_custom_function(self):
        formula = "@custom_function(3,2,3)"
        expected_name = "custom_function"
        expected_children = ["3", "2", "3"]
        root = parse_formula(formula)
        self.check_structure(root, expected_name, expected_children)

    def test_nested_function(self):
        formula = "@custom_function(@jsonpath($element.[*]), 1)"
        expected_name = "custom_function"
        expected_children = [("jsonpath", ["$element.[*]"]), "1"]
        root = parse_formula(formula)
        self.check_structure(root, expected_name, expected_children)

    def test_double_nested_function(self):
        formula = "@custom_function(@jsonpath($element.[0].[0]), @jsonpath($element.[1].[0]))"
        expected_name = "custom_function"
        expected_children = [("jsonpath", ["$element.[0].[0]"]), ("jsonpath", ["$element.[1].[0]"])]
        root = parse_formula(formula)
        self.check_structure(root, expected_name, expected_children)

    def test_complex_nest(self):
        formula = "@jsonpath(@custom_function1(@custom_function2($element.[*])))"
        expected_name = "jsonpath"
        expected_children = [("custom_function1", [("custom_function2", ["$element.[*]"])])]
        root = parse_formula(formula)
        self.check_structure(root, expected_name, expected_children)

if __name__ == '__main__':
    unittest.main()
