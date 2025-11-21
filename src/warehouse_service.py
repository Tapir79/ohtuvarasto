from warehouse import Warehouse


class WarehouseService:
    """Service class to manage multiple warehouses."""

    def __init__(self):
        self._warehouses = {}
        self._next_id = 1

    def create_warehouse(self, name, tilavuus, saldo=0):
        """Create a new warehouse with given name, capacity and initial balance.

        Args:
            name: Name of the warehouse
            tilavuus: Capacity of the warehouse
            saldo: Initial balance (default 0)

        Returns:
            The ID of the created warehouse
        """
        warehouse_id = self._next_id
        self._next_id += 1

        warehouse = Warehouse(warehouse_id, name, tilavuus, saldo)
        self._warehouses[warehouse_id] = warehouse

        return warehouse_id

    def get_warehouse(self, warehouse_id):
        """Get a warehouse by ID.

        Args:
            warehouse_id: ID of the warehouse

        Returns:
            Dictionary with warehouse data or None if not found
        """
        if warehouse_id not in self._warehouses:
            return None

        return self._warehouses[warehouse_id].to_dict()

    def get_warehouse_object(self, warehouse_id):
        """Get a warehouse object by ID.

        Args:
            warehouse_id: ID of the warehouse

        Returns:
            Warehouse object or None if not found
        """
        return self._warehouses.get(warehouse_id)

    def list_warehouses(self):
        """List all warehouses.

        Returns:
            List of dictionaries with warehouse data
        """
        return [self._warehouses[warehouse_id].to_dict()
                for warehouse_id in sorted(self._warehouses.keys())]

    def update_warehouse(self, warehouse_id, name=None, tilavuus=None,
                         saldo=None):
        """Update warehouse properties.

        Args:
            warehouse_id: ID of the warehouse
            name: New name (optional)
            tilavuus: New capacity (optional)
            saldo: New balance (optional)

        Returns:
            True if successful, False if warehouse not found
        """
        warehouse = self.get_warehouse_object(warehouse_id)
        if warehouse is None:
            return False

        warehouse.update(name=name, tilavuus=tilavuus, saldo=saldo)
        return True

    def add_to_warehouse(self, warehouse_id, maara):
        """Add items to a warehouse.

        Args:
            warehouse_id: ID of the warehouse
            maara: Amount to add

        Returns:
            True if successful, False if warehouse not found
        """
        warehouse = self.get_warehouse_object(warehouse_id)
        if warehouse is None:
            return False

        warehouse.add_items(maara)
        return True

    def remove_from_warehouse(self, warehouse_id, maara):
        """Remove items from a warehouse.

        Args:
            warehouse_id: ID of the warehouse
            maara: Amount to remove

        Returns:
            The actual amount removed, or None if warehouse not found
        """
        warehouse = self.get_warehouse_object(warehouse_id)
        if warehouse is None:
            return None

        return warehouse.remove_items(maara)

    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse.

        Args:
            warehouse_id: ID of the warehouse

        Returns:
            True if successful, False if warehouse not found
        """
        if warehouse_id not in self._warehouses:
            return False

        del self._warehouses[warehouse_id]
        return True
