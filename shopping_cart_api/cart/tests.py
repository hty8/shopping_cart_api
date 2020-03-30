from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cart, User, DeliveryCost
from products.models import Category, Product


class UserTests(APITestCase):
    def test_create_user(self):
        self.test_user = User.objects.create(name='Test User Name')

        data = {'name': self.test_user.name}
        response = self.client.post('/cart/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeliveryCostTests(APITestCase):

    def test_create_delivery_cost(self):
        self.test_delivery_cost = DeliveryCost.objects.create(status="Active",
                                                              cost_per_delivery=10,
                                                              cost_per_product=4.50,
                                                              fixed_cost=2.99)
        data = {"status": self.test_delivery_cost.status,
                "cost_per_delivery": self.test_delivery_cost.cost_per_delivery,
                "cost_per_product": self.test_delivery_cost.cost_per_product,
                "fixed_cost": self.test_delivery_cost.fixed_cost}
        response = self.client.post('/cart/delivery-cost/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CartTests(APITestCase):

    def test_create_cart_item(self):
        self.test_user = User.objects.create(name='Test User')
        self.test_category = Category.objects.create(title='Test Category',
                                                     parent_category_id=None)

        self.test_product = Product.objects.create(category=self.test_category,
                                                   title='Test Product',
                                                   price=10.00)
        data = {'user': self.test_user.id,
                'item': self.test_product.id,
                'quantity': 1}
        response = self.client.post('/cart/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().item.title, self.test_product.title)

    def test_checkout_by_user(self):
        self.test_user = User.objects.create(name='Test User 3')
        self.test_category = Category.objects.create(title='Test Category 3',
                                                     parent_category_id=1)

        self.test_product = Product.objects.create(category=self.test_category,
                                                   title='Test Product3',
                                                   price=30.00)

        self.test_cart_item = Cart.objects.create(user=self.test_user,
                                                  item=self.test_product,
                                                  quantity=4)

        self.test_delivery_cost = DeliveryCost.objects.create(status="Active",
                                                              cost_per_delivery=10,
                                                              cost_per_product=4.50,
                                                              fixed_cost=2.99)

        response = self.client.get("/cart/cart/checkout/{0}/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('checkout_details', False).get('products', False), False)
        self.assertNotEqual(response.data.get('checkout_details', False).get('total', False), False)
        self.assertNotEqual(response.data.get('checkout_details', False).get('amount', False), False)
