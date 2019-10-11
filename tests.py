from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

sample_shirt_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_shirt = {
    'title': 'Teddy',
    'image': 'https://cdn.shopify.com/s/files/1/2166/8231/products/embroidered-sweater-1_600x.jpg?v=1565369508',
    'price': "$30"
}
sample_form_data = {
    'title': sample_shirt['title'],
    'image': sample_shirt['image'],
    'price': sample_shirt['price']
}

class PlaylistsTests(TestCase):
    def setUp(self):
        # test setup
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        # test homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'shirt', result.data)

    def test_new(self):
        """Test the new shirt creation page."""
        result = self.client.get('/shirts/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Shirt', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_shirt(self, mock_find):
        """Test showing a single playlist."""
        mock_find.return_value = sample_shirt

        result = self.client.get(f'/shirts/{sample_shirt_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'shirts', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_shirt(self, mock_find):
        """Test editing a single shirt"""
        mock_find.return_value = sample_shirt

        result = self.client.get(f'/shirts/{sample_shirt_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'shirts', result.data)
    
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_shirt(self, mock_insert):
        """Test submitting a new shrit."""
        result = self.client.post('/shirts', data=sample_form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_shirt)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_shirt(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/shirt/{sample_shirt_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_shirt_id})

if __name__ == '__main__':
    unittest_main()
