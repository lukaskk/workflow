from django.test import TestCase, Client
from django.urls import reverse
from .models import Order, OrderPhoto
from django.core.files.uploadedfile import SimpleUploadedFile
import os
 # Assuming the zip file will be larger than an empty zip file size
class OrderPhotoZipDownloadEdgeCasesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = 'download_photos_zip'
        self.test_file_path = 'test_media/edge_case_photo.jpg'
        with open(self.test_file_path, 'wb') as file:
            file.write(b'Edge case file content')
        self.test_photo = SimpleUploadedFile(name='edge_case_photo.jpg', content=open(self.test_file_path, 'rb').read(), content_type='image/jpeg')
        self.order = Order.objects.create(name='EdgeCaseOrder', city='EdgeCity', street='EdgeStreet')
        OrderPhoto.objects.create(order=self.order, photo=self.test_photo)

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_download_photos_zip_empty_order_name(self):
        Order.objects.create(name='', city='NoNameCity', street='NoNameStreet')
        response = self.client.get(reverse(self.base_url, kwargs={'name': ''}))
        self.assertEqual(response.status_code, 404)

    def test_download_photos_zip_order_with_spaces_in_name(self):
        Order.objects.create(name='Order With Spaces', city='SpaceCity', street='SpaceStreet')
        response = self.client.get(reverse(self.base_url, kwargs={'name': 'Order With Spaces'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/zip', response['Content-Type'])
        self.assertTrue('Order With Spaces_photos.zip' in response['Content-Disposition'])

    def test_download_photos_zip_case_insensitive_order_name(self):
        response = self.client.get(reverse(self.base_url, kwargs={'name': 'testorder'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/zip', response['Content-Type'])
        self.assertTrue('TestOrder_photos.zip' in response['Content-Disposition'])

    def test_download_photos_zip_with_nonexistent_file(self):
        OrderPhoto.objects.create(order=self.order, photo=SimpleUploadedFile(name='nonexistent_photo.jpg', content=b'', content_type='image/jpeg'))
        response = self.client.get(reverse(self.base_url, kwargs={'name': 'EdgeCaseOrder'}))
        self.assertEqual(response.status_code, 200)
        # Assuming the application handles missing files gracefully and still returns a zip (possibly empty)
        self.assertIn('application/zip', response['Content-Type'])
        self.assertTrue('EdgeCaseOrder_photos.zip' in response['Content-Disposition'])
