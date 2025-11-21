"""Validation utilities for warehouse data."""


class ValidationError(Exception):
    """Custom exception for validation errors."""

    def __init__(self, errors):
        """Initialize with a list of error messages.

        Args:
            errors: List of error message strings
        """
        self.errors = errors if isinstance(errors, list) else [errors]
        super().__init__(str(self.errors))


def validate_warehouse_name(name):
    """Validate warehouse name.

    Args:
        name: Name string to validate

    Returns:
        Stripped name if valid

    Raises:
        ValidationError: If name is invalid
    """
    if not name or not name.strip():
        raise ValidationError('Name is required')
    return name.strip()


def validate_positive_number(value_str, field_name):
    """Validate a positive number field.

    Args:
        value_str: String value to validate
        field_name: Name of the field for error messages

    Returns:
        Float value if valid

    Raises:
        ValidationError: If value is invalid
    """
    try:
        value = float(value_str)
        if value < 0:
            raise ValidationError(f'{field_name} must be non-negative')
        return value
    except ValueError as exc:
        raise ValidationError(f'{field_name} must be a valid number') from exc


def validate_warehouse_creation(name, tilavuus_str, saldo_str='0'):
    """Validate warehouse creation data.

    Args:
        name: Warehouse name
        tilavuus_str: Capacity as string
        saldo_str: Initial balance as string (default '0')

    Returns:
        Tuple of (name, tilavuus, saldo) if valid

    Raises:
        ValidationError: If any validation fails
    """
    errors = []

    # Validate name
    try:
        validated_name = validate_warehouse_name(name)
    except ValidationError as e:
        errors.extend(e.errors)
        validated_name = name

    # Validate capacity
    try:
        tilavuus = validate_positive_number(tilavuus_str, 'Capacity')
    except ValidationError as e:
        errors.extend(e.errors)
        tilavuus = 0

    # Validate balance
    try:
        saldo = validate_positive_number(saldo_str, 'Balance')
    except ValidationError as e:
        errors.extend(e.errors)
        saldo = 0

    if errors:
        raise ValidationError(errors)

    return validated_name, tilavuus, saldo


def validate_warehouse_update(name, tilavuus_str, saldo_str):
    """Validate warehouse update data.

    Args:
        name: Warehouse name
        tilavuus_str: Capacity as string
        saldo_str: Balance as string

    Returns:
        Tuple of (name, tilavuus, saldo) if valid

    Raises:
        ValidationError: If any validation fails
    """
    return validate_warehouse_creation(name, tilavuus_str, saldo_str)


def validate_amount(amount_str):
    """Validate an amount for add/remove operations.

    Args:
        amount_str: Amount as string

    Returns:
        Float value if valid

    Raises:
        ValidationError: If amount is invalid
    """
    return validate_positive_number(amount_str, 'Amount')
