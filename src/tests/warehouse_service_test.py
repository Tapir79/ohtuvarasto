import unittest
from warehouse_service import WarehouseService
from warehouse import Warehouse


class TestWarehouseService(unittest.TestCase):
    def setUp(self):
        self.service = WarehouseService()

    def test_create_warehouse(self):
        warehouse = Warehouse("Test Warehouse", 100.0, 20.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        self.assertEqual(warehouse_id, 1)

        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertIsNotNone(warehouse_data)
        self.assertEqual(warehouse_data['name'], "Test Warehouse")
        self.assertAlmostEqual(warehouse_data['tilavuus'], 100.0)
        self.assertAlmostEqual(warehouse_data['saldo'], 20.0)

    def test_create_multiple_warehouses(self):
        warehouse1 = Warehouse("Warehouse 1", 100.0)
        warehouse2 = Warehouse("Warehouse 2", 200.0)
        id1 = self.service.create_warehouse(warehouse1)
        id2 = self.service.create_warehouse(warehouse2)

        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_get_nonexistent_warehouse(self):
        warehouse = self.service.get_warehouse(999)
        self.assertIsNone(warehouse)

    def test_list_empty_warehouses(self):
        warehouses = self.service.list_warehouses()
        self.assertEqual(len(warehouses), 0)

    def test_list_warehouses(self):
        self.service.create_warehouse(Warehouse("Warehouse 1", 100.0))
        self.service.create_warehouse(Warehouse("Warehouse 2", 200.0))

        warehouses = self.service.list_warehouses()
        self.assertEqual(len(warehouses), 2)
        self.assertEqual(warehouses[0]['name'], "Warehouse 1")
        self.assertEqual(warehouses[1]['name'], "Warehouse 2")

    def test_update_warehouse_name(self):
        warehouse = Warehouse("Old Name", 100.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        result = self.service.update_warehouse(warehouse_id, name="New Name")

        self.assertTrue(result)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse_data['name'], "New Name")

    def test_update_warehouse_capacity(self):
        warehouse = Warehouse("Test", 100.0, 50.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        result = self.service.update_warehouse(warehouse_id, tilavuus=200.0)

        self.assertTrue(result)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['tilavuus'], 200.0)
        self.assertAlmostEqual(warehouse_data['saldo'], 50.0)

    def test_update_warehouse_balance(self):
        warehouse = Warehouse("Test", 100.0, 50.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        result = self.service.update_warehouse(warehouse_id, saldo=30.0)

        self.assertTrue(result)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['saldo'], 30.0)

    def test_update_nonexistent_warehouse(self):
        result = self.service.update_warehouse(999, name="New Name")
        self.assertFalse(result)

    def test_add_to_warehouse(self):
        warehouse = Warehouse("Test", 100.0, 20.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        result = self.service.add_to_warehouse(warehouse_id, 30.0)

        self.assertTrue(result)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['saldo'], 50.0)

    def test_add_to_nonexistent_warehouse(self):
        result = self.service.add_to_warehouse(999, 10.0)
        self.assertFalse(result)

    def test_add_negative_amount(self):
        warehouse = Warehouse("Test", 100.0, 20.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        self.service.add_to_warehouse(warehouse_id, -10.0)

        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['saldo'], 20.0)

    def test_remove_from_warehouse(self):
        warehouse = Warehouse("Test", 100.0, 50.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        removed = self.service.remove_from_warehouse(warehouse_id, 20.0)

        self.assertAlmostEqual(removed, 20.0)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['saldo'], 30.0)

    def test_remove_from_nonexistent_warehouse(self):
        removed = self.service.remove_from_warehouse(999, 10.0)
        self.assertIsNone(removed)

    def test_remove_more_than_available(self):
        warehouse = Warehouse("Test", 100.0, 50.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        removed = self.service.remove_from_warehouse(warehouse_id, 80.0)

        self.assertAlmostEqual(removed, 50.0)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse_data['saldo'], 0.0)

    def test_delete_warehouse(self):
        warehouse = Warehouse("Test", 100.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        result = self.service.delete_warehouse(warehouse_id)

        self.assertTrue(result)
        warehouse_data = self.service.get_warehouse(warehouse_id)
        self.assertIsNone(warehouse_data)

    def test_delete_nonexistent_warehouse(self):
        result = self.service.delete_warehouse(999)
        self.assertFalse(result)

    def test_warehouse_paljonko_mahtuu(self):
        warehouse = Warehouse("Test", 100.0, 30.0)
        warehouse_id = self.service.create_warehouse(warehouse)
        warehouse_data = self.service.get_warehouse(warehouse_id)

        self.assertAlmostEqual(warehouse_data['paljonko_mahtuu'], 70.0)
