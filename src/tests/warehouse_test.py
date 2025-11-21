import unittest
from warehouse import Warehouse


class TestWarehouse(unittest.TestCase):
    def test_create_warehouse(self):
        warehouse = Warehouse("Test", 100.0, 20.0, warehouse_id=1)
        self.assertEqual(warehouse.id, 1)
        self.assertEqual(warehouse.name, "Test")
        self.assertAlmostEqual(warehouse.tilavuus, 100.0)
        self.assertAlmostEqual(warehouse.saldo, 20.0)
        self.assertAlmostEqual(warehouse.paljonko_mahtuu, 80.0)

    def test_update_name(self):
        warehouse = Warehouse("Old Name", 100.0, 20.0, warehouse_id=1)
        warehouse.update(name="New Name")
        self.assertEqual(warehouse.name, "New Name")
        self.assertAlmostEqual(warehouse.tilavuus, 100.0)
        self.assertAlmostEqual(warehouse.saldo, 20.0)

    def test_update_capacity(self):
        warehouse = Warehouse("Test", 100.0, 20.0, warehouse_id=1)
        warehouse.update(tilavuus=200.0)
        self.assertAlmostEqual(warehouse.tilavuus, 200.0)
        self.assertAlmostEqual(warehouse.saldo, 20.0)

    def test_update_balance(self):
        warehouse = Warehouse("Test", 100.0, 20.0, warehouse_id=1)
        warehouse.update(saldo=50.0)
        self.assertAlmostEqual(warehouse.saldo, 50.0)
        self.assertAlmostEqual(warehouse.tilavuus, 100.0)

    def test_add_items(self):
        warehouse = Warehouse("Test", 100.0, 20.0, warehouse_id=1)
        warehouse.add_items(30.0)
        self.assertAlmostEqual(warehouse.saldo, 50.0)

    def test_remove_items(self):
        warehouse = Warehouse("Test", 100.0, 50.0, warehouse_id=1)
        removed = warehouse.remove_items(20.0)
        self.assertAlmostEqual(removed, 20.0)
        self.assertAlmostEqual(warehouse.saldo, 30.0)

    def test_to_dict(self):
        warehouse = Warehouse("Test", 100.0, 20.0, warehouse_id=1)
        data = warehouse.to_dict()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Test")
        self.assertAlmostEqual(data['tilavuus'], 100.0)
        self.assertAlmostEqual(data['saldo'], 20.0)
        self.assertAlmostEqual(data['paljonko_mahtuu'], 80.0)
