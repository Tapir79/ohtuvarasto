from varasto import Varasto


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

        self._warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(tilavuus, saldo)
        }

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

        warehouse_data = self._warehouses[warehouse_id]
        varasto = warehouse_data['varasto']

        return {
            'id': warehouse_data['id'],
            'name': warehouse_data['name'],
            'tilavuus': varasto.tilavuus,
            'saldo': varasto.saldo,
            'paljonko_mahtuu': varasto.paljonko_mahtuu()
        }

    def list_warehouses(self):
        """List all warehouses.

        Returns:
            List of dictionaries with warehouse data
        """
        warehouses = []
        for warehouse_id in sorted(self._warehouses.keys()):
            warehouses.append(self.get_warehouse(warehouse_id))
        return warehouses

    def update_warehouse(
            self,
            warehouse_id,
            name=None,
            tilavuus=None,
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
        if warehouse_id not in self._warehouses:
            return False

        warehouse_data = self._warehouses[warehouse_id]

        if name is not None:
            warehouse_data['name'] = name

        if tilavuus is not None or saldo is not None:
            current_varasto = warehouse_data['varasto']
            new_tilavuus = (tilavuus if tilavuus is not None
                            else current_varasto.tilavuus)
            new_saldo = (saldo if saldo is not None
                         else current_varasto.saldo)
            warehouse_data['varasto'] = Varasto(new_tilavuus, new_saldo)

        return True

    def add_to_warehouse(self, warehouse_id, maara):
        """Add items to a warehouse.

        Args:
            warehouse_id: ID of the warehouse
            maara: Amount to add

        Returns:
            True if successful, False if warehouse not found
        """
        if warehouse_id not in self._warehouses:
            return False

        warehouse_data = self._warehouses[warehouse_id]
        warehouse_data['varasto'].lisaa_varastoon(maara)
        return True

    def remove_from_warehouse(self, warehouse_id, maara):
        """Remove items from a warehouse.

        Args:
            warehouse_id: ID of the warehouse
            maara: Amount to remove

        Returns:
            The actual amount removed, or None if warehouse not found
        """
        if warehouse_id not in self._warehouses:
            return None

        warehouse_data = self._warehouses[warehouse_id]
        return warehouse_data['varasto'].ota_varastosta(maara)

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
