"""Tests for Flask web application and warehouse service."""
import unittest
from app import app
from warehouse_service import WarehouseService
from varasto import Varasto


class TestWarehouseService(unittest.TestCase):
    """Tests for the WarehouseService class."""
    
    def setUp(self):
        """Set up a fresh warehouse service for each test."""
        self.service = WarehouseService()
    
    def test_create_warehouse(self):
        """Test creating a new warehouse."""
        warehouse_id = self.service.create_warehouse("Test", 100, 50)
        self.assertEqual(warehouse_id, 1)
        
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertIsNotNone(warehouse)
        self.assertEqual(warehouse['name'], "Test")
        self.assertEqual(warehouse['varasto'].tilavuus, 100)
        self.assertEqual(warehouse['varasto'].saldo, 50)
    
    def test_get_nonexistent_warehouse(self):
        """Test getting a warehouse that doesn't exist."""
        warehouse = self.service.get_warehouse(999)
        self.assertIsNone(warehouse)
    
    def test_get_all_warehouses(self):
        """Test getting all warehouses."""
        self.assertEqual(len(self.service.get_all_warehouses()), 0)
        
        self.service.create_warehouse("Test1", 100, 0)
        self.service.create_warehouse("Test2", 200, 0)
        
        warehouses = self.service.get_all_warehouses()
        self.assertEqual(len(warehouses), 2)
    
    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        warehouse_id = self.service.create_warehouse("Test", 100, 0)
        
        self.assertTrue(self.service.delete_warehouse(warehouse_id))
        self.assertIsNone(self.service.get_warehouse(warehouse_id))
    
    def test_delete_nonexistent_warehouse(self):
        """Test deleting a warehouse that doesn't exist."""
        self.assertFalse(self.service.delete_warehouse(999))
    
    def test_update_warehouse_name(self):
        """Test updating warehouse name."""
        warehouse_id = self.service.create_warehouse("Test", 100, 0)
        
        self.service.update_warehouse(warehouse_id, name="Updated")
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['name'], "Updated")
    
    def test_update_warehouse_capacity(self):
        """Test updating warehouse capacity."""
        warehouse_id = self.service.create_warehouse("Test", 100, 50)
        
        self.service.update_warehouse(warehouse_id, tilavuus=200)
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['varasto'].tilavuus, 200)
        self.assertEqual(warehouse['varasto'].saldo, 50)
    
    def test_update_warehouse_saldo(self):
        """Test updating warehouse balance."""
        warehouse_id = self.service.create_warehouse("Test", 100, 50)
        
        self.service.update_warehouse(warehouse_id, saldo=75)
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['varasto'].saldo, 75)
    
    def test_update_nonexistent_warehouse(self):
        """Test updating a warehouse that doesn't exist."""
        self.assertFalse(self.service.update_warehouse(999, name="Test"))
    
    def test_add_to_warehouse(self):
        """Test adding items to a warehouse."""
        warehouse_id = self.service.create_warehouse("Test", 100, 50)
        
        self.service.add_to_warehouse(warehouse_id, 20)
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['varasto'].saldo, 70)
    
    def test_add_to_nonexistent_warehouse(self):
        """Test adding to a warehouse that doesn't exist."""
        self.assertFalse(self.service.add_to_warehouse(999, 10))
    
    def test_remove_from_warehouse(self):
        """Test removing items from a warehouse."""
        warehouse_id = self.service.create_warehouse("Test", 100, 50)
        
        removed = self.service.remove_from_warehouse(warehouse_id, 20)
        self.assertEqual(removed, 20)
        warehouse = self.service.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['varasto'].saldo, 30)
    
    def test_remove_from_nonexistent_warehouse(self):
        """Test removing from a warehouse that doesn't exist."""
        removed = self.service.remove_from_warehouse(999, 10)
        self.assertIsNone(removed)


class TestFlaskApp(unittest.TestCase):
    """Tests for the Flask application routes."""
    
    def setUp(self):
        """Set up test client and initialize app in testing mode."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        # Reset the warehouse service for each test
        from app import warehouse_service
        warehouse_service.warehouses = {}
        warehouse_service.next_id = 1
    
    def test_index_redirect(self):
        """Test that root redirects to warehouses list."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/warehouses', response.location)
    
    def test_list_warehouses_empty(self):
        """Test listing warehouses when none exist."""
        response = self.client.get('/warehouses')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)
    
    def test_list_warehouses_with_data(self):
        """Test listing warehouses with data."""
        # Create a warehouse first
        self.client.post('/warehouses', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.get('/warehouses')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
    
    def test_new_warehouse_form(self):
        """Test the new warehouse form page."""
        response = self.client.get('/warehouses/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)
    
    def test_create_warehouse_valid(self):
        """Test creating a warehouse with valid data."""
        response = self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)
    
    def test_create_warehouse_missing_name(self):
        """Test creating a warehouse without a name."""
        response = self.client.post('/warehouses', data={
            'name': '',
            'tilavuus': '100',
            'alku_saldo': '0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name is required', response.data)
    
    def test_create_warehouse_invalid_capacity(self):
        """Test creating a warehouse with invalid capacity."""
        response = self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '-10',
            'alku_saldo': '0'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Capacity must be greater than 0', response.data)
    
    def test_create_warehouse_invalid_balance(self):
        """Test creating a warehouse with negative balance."""
        response = self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '-10'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cannot be negative', response.data)
    
    def test_warehouse_detail(self):
        """Test viewing warehouse detail page."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.get('/warehouses/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)
        self.assertIn(b'100.0', response.data)
    
    def test_warehouse_detail_not_found(self):
        """Test viewing a warehouse that doesn't exist."""
        response = self.client.get('/warehouses/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'not found', response.data)
    
    def test_add_items(self):
        """Test adding items to a warehouse."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/warehouses/1/add', data={
            'amount': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Added', response.data)
    
    def test_add_items_invalid_amount(self):
        """Test adding invalid amount to a warehouse."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/warehouses/1/add', data={
            'amount': '-10'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'greater than 0', response.data)
    
    def test_remove_items(self):
        """Test removing items from a warehouse."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/warehouses/1/remove', data={
            'amount': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Removed', response.data)
    
    def test_edit_warehouse_form(self):
        """Test the edit warehouse form page."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.get('/warehouses/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)
    
    def test_update_warehouse(self):
        """Test updating a warehouse."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/warehouses/1/edit', data={
            'name': 'Updated',
            'tilavuus': '200',
            'saldo': '75'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated', response.data)
        self.assertIn(b'updated successfully', response.data)
    
    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        # Create a warehouse
        self.client.post('/warehouses', data={
            'name': 'Test',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/warehouses/1/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)
