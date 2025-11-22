import unittest
from app import app, warehouse_service


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Reset the warehouse service for each test
        warehouse_service._warehouses = {}
        warehouse_service._next_id = 1

    def test_list_warehouses_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses found', response.data)

    def test_create_warehouse_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse_post_valid(self):
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)

    def test_create_warehouse_post_missing_name(self):
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100',
            'saldo': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)

    def test_create_warehouse_post_invalid_capacity(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': 'invalid',
            'saldo': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Capacity must be a valid number', response.data)

    def test_create_warehouse_post_negative_capacity(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': '-10',
            'saldo': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Capacity must be non-negative', response.data)

    def test_view_warehouse(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertIn(b'100.00', response.data)
        self.assertIn(b'20.00', response.data)

    def test_view_nonexistent_warehouse(self):
        response = self.client.get('/warehouse/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse not found', response.data)

    def test_edit_warehouse_get(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.get('/warehouse/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)
        self.assertIn(b'Test Warehouse', response.data)

    def test_edit_warehouse_post_valid(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/edit', data={
            'name': 'Updated Warehouse',
            'tilavuus': '150',
            'saldo': '30'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Warehouse', response.data)
        self.assertIn(b'150.00', response.data)
        self.assertIn(b'30.00', response.data)

    def test_edit_warehouse_post_missing_name(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/edit', data={
            'name': '',
            'tilavuus': '150',
            'saldo': '30'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)

    def test_add_items(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/add', data={
            'maara': '30'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Added 30', response.data)

    def test_add_items_invalid_amount(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/add', data={
            'maara': 'invalid'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amount must be a valid number', response.data)

    def test_add_items_negative_amount(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/add', data={
            'maara': '-10'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amount must be non-negative', response.data)

    def test_remove_items(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '50'
        })
        
        response = self.client.post('/warehouse/1/remove', data={
            'maara': '20'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Removed 20', response.data)

    def test_remove_items_invalid_amount(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '50'
        })
        
        response = self.client.post('/warehouse/1/remove', data={
            'maara': 'invalid'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Amount must be a valid number', response.data)

    def test_delete_warehouse(self):
        # Create a warehouse first
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'saldo': '20'
        })
        
        response = self.client.post('/warehouse/1/delete', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)
        
        # Verify warehouse is deleted
        response = self.client.get('/warehouse/1', follow_redirects=True)
        self.assertIn(b'Warehouse not found', response.data)

    def test_delete_nonexistent_warehouse(self):
        response = self.client.post('/warehouse/999/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse not found', response.data)
