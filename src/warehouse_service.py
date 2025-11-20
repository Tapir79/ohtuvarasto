"""Service layer for managing warehouse instances."""
from varasto import Varasto


class WarehouseService:
    """Service to manage multiple warehouse instances in memory."""
    
    def __init__(self):
        """Initialize the service with empty warehouse storage."""
        self.warehouses = {}
        self.next_id = 1
    
    def create_warehouse(self, name, tilavuus, alku_saldo=0):
        """
        Create a new warehouse instance.
        
        Args:
            name: Display name for the warehouse
            tilavuus: Maximum capacity of the warehouse
            alku_saldo: Initial inventory (default 0)
            
        Returns:
            The warehouse ID
        """
        warehouse_id = self.next_id
        self.warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        self.next_id += 1
        return warehouse_id
    
    def get_warehouse(self, warehouse_id):
        """
        Get a warehouse by ID.
        
        Args:
            warehouse_id: The warehouse ID
            
        Returns:
            Dictionary with warehouse data or None if not found
        """
        return self.warehouses.get(warehouse_id)
    
    def get_all_warehouses(self):
        """
        Get all warehouses.
        
        Returns:
            List of all warehouse dictionaries
        """
        return list(self.warehouses.values())
    
    def delete_warehouse(self, warehouse_id):
        """
        Delete a warehouse.
        
        Args:
            warehouse_id: The warehouse ID
            
        Returns:
            True if deleted, False if not found
        """
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]
            return True
        return False
    
    def update_warehouse(self, warehouse_id, name=None, tilavuus=None, saldo=None):
        """
        Update warehouse properties.
        
        Args:
            warehouse_id: The warehouse ID
            name: New name (optional)
            tilavuus: New capacity (optional)
            saldo: New balance (optional)
            
        Returns:
            True if updated, False if not found
        """
        warehouse = self.warehouses.get(warehouse_id)
        if not warehouse:
            return False
        
        if name is not None:
            warehouse['name'] = name
        
        # If we need to change tilavuus or saldo, create a new Varasto instance
        if tilavuus is not None or saldo is not None:
            current_varasto = warehouse['varasto']
            new_tilavuus = tilavuus if tilavuus is not None else current_varasto.tilavuus
            new_saldo = saldo if saldo is not None else current_varasto.saldo
            warehouse['varasto'] = Varasto(new_tilavuus, new_saldo)
        
        return True
    
    def add_to_warehouse(self, warehouse_id, amount):
        """
        Add items to a warehouse.
        
        Args:
            warehouse_id: The warehouse ID
            amount: Amount to add
            
        Returns:
            True if successful, False if warehouse not found
        """
        warehouse = self.warehouses.get(warehouse_id)
        if not warehouse:
            return False
        
        warehouse['varasto'].lisaa_varastoon(amount)
        return True
    
    def remove_from_warehouse(self, warehouse_id, amount):
        """
        Remove items from a warehouse.
        
        Args:
            warehouse_id: The warehouse ID
            amount: Amount to remove
            
        Returns:
            Amount actually removed, or None if warehouse not found
        """
        warehouse = self.warehouses.get(warehouse_id)
        if not warehouse:
            return None
        
        return warehouse['varasto'].ota_varastosta(amount)
