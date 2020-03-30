from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product


class CategoryTests(APITestCase):
    def test_create_category(self):
        self.test_category = Category.objects.create(title='Test Category',
                                                     parent_category_id=None)

        data = {'title': self.test_category.title,
                'parent_category_id': self.test_category.parent_category_id}
        response = self.client.post('/products/category/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductTests(APITestCase):
    def test_create_product(self):
        self.test_category = Category.objects.create(title='Test Category',
                                                     parent_category_id=None)
        self.test_product = Product.objects.create(category=self.test_category,
                                                   title='Test Product',
                                                   price=100.00)

        data = {'category': self.test_category.id,
                'title': self.test_product.title,
                'price': self.test_product.price}
        response = self.client.post('/products/product/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
