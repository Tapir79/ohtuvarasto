import unittest
from validation import (ValidationError, validate_warehouse_name,
                        validate_positive_number, validate_warehouse_creation,
                        validate_amount)


class TestValidation(unittest.TestCase):
    def test_validate_warehouse_name_valid(self):
        name = validate_warehouse_name("  Test Warehouse  ")
        self.assertEqual(name, "Test Warehouse")

    def test_validate_warehouse_name_empty(self):
        with self.assertRaises(ValidationError) as context:
            validate_warehouse_name("")
        self.assertIn('Name is required', context.exception.errors)

    def test_validate_positive_number_valid(self):
        value = validate_positive_number("100.5", "Capacity")
        self.assertAlmostEqual(value, 100.5)

    def test_validate_positive_number_negative(self):
        with self.assertRaises(ValidationError) as context:
            validate_positive_number("-10", "Capacity")
        self.assertIn('Capacity must be non-negative',
                      context.exception.errors)

    def test_validate_positive_number_invalid(self):
        with self.assertRaises(ValidationError) as context:
            validate_positive_number("abc", "Capacity")
        self.assertIn('Capacity must be a valid number',
                      context.exception.errors)

    def test_validate_warehouse_creation_valid(self):
        name, tilavuus, saldo = validate_warehouse_creation(
            "Test", "100", "20")
        self.assertEqual(name, "Test")
        self.assertAlmostEqual(tilavuus, 100.0)
        self.assertAlmostEqual(saldo, 20.0)

    def test_validate_warehouse_creation_multiple_errors(self):
        with self.assertRaises(ValidationError) as context:
            validate_warehouse_creation("", "abc", "-10")
        self.assertEqual(len(context.exception.errors), 3)

    def test_validate_amount_valid(self):
        amount = validate_amount("50.5")
        self.assertAlmostEqual(amount, 50.5)

    def test_validate_amount_negative(self):
        with self.assertRaises(ValidationError):
            validate_amount("-10")

    def test_validation_error_with_list(self):
        error = ValidationError(['Error 1', 'Error 2'])
        self.assertEqual(len(error.errors), 2)

    def test_validation_error_with_string(self):
        error = ValidationError('Single error')
        self.assertEqual(len(error.errors), 1)
        self.assertEqual(error.errors[0], 'Single error')
