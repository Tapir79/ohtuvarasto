from varasto import Varasto


class Warehouse:
    """Domain class representing a warehouse with a unique ID and name."""

    def __init__(self, warehouse_id, name, tilavuus, saldo=0):
        """Initialize a warehouse.

        Args:
            warehouse_id: Unique identifier for the warehouse
            name: Name of the warehouse
            tilavuus: Capacity of the warehouse
            saldo: Initial balance (default 0)
        """
        self.id = warehouse_id
        self.name = name
        self._varasto = Varasto(tilavuus, saldo)

    @property
    def tilavuus(self):
        """Get the warehouse capacity."""
        return self._varasto.tilavuus

    @property
    def saldo(self):
        """Get the current balance."""
        return self._varasto.saldo

    @property
    def paljonko_mahtuu(self):
        """Get the available space."""
        return self._varasto.paljonko_mahtuu()

    def update(self, name=None, tilavuus=None, saldo=None):
        """Update warehouse properties.

        Args:
            name: New name (optional)
            tilavuus: New capacity (optional)
            saldo: New balance (optional)
        """
        if name is not None:
            self.name = name

        if tilavuus is not None or saldo is not None:
            new_tilavuus = (tilavuus if tilavuus is not None
                            else self._varasto.tilavuus)
            new_saldo = (saldo if saldo is not None
                         else self._varasto.saldo)
            self._varasto = Varasto(new_tilavuus, new_saldo)

    def add_items(self, maara):
        """Add items to the warehouse.

        Args:
            maara: Amount to add
        """
        self._varasto.lisaa_varastoon(maara)

    def remove_items(self, maara):
        """Remove items from the warehouse.

        Args:
            maara: Amount to remove

        Returns:
            The actual amount removed
        """
        return self._varasto.ota_varastosta(maara)

    def to_dict(self):
        """Convert warehouse to dictionary representation.

        Returns:
            Dictionary with warehouse data
        """
        return {
            'id': self.id,
            'name': self.name,
            'tilavuus': self.tilavuus,
            'saldo': self.saldo,
            'paljonko_mahtuu': self.paljonko_mahtuu
        }
