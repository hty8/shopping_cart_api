from rest_framework.test import APITestCase
from rest_framework import status
from .models import Campaign, Coupon
from products.models import Category, Product


class CampaignTests(APITestCase):

    def test_create_campaign(self):
        self.test_category = Category.objects.create(title='Test Category4',
                                                     parent_category_id=None)

        data = {'discount_type': 'Rate',
                'discount_rate': '10',
                'discount_amount': None,
                'min_purchased_items': 3,
                'apply_to': 'Category',
                'target_product': None,
                'target_category': self.test_category.id}

        response = self.client.post('/discounts/campaign/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Campaign.objects.get().min_purchased_items, 3)

    def test_get_campaign(self):
        self.test_category = Category.objects.create(title='Test Category5',
                                                     parent_category_id=None)

        self.test_product = Product.objects.create(category=self.test_category,
                                                   title='Test Product4',
                                                   price=100.00)

        self.test_campaign = Campaign.objects.create(discount_type='Fixed',
                                                     discount_rate=None,
                                                     discount_amount=5,
                                                     min_purchased_items=2,
                                                     apply_to='Product',
                                                     target_product=self.test_product,
                                                     target_category=None)

        response = self.client.get("/discounts/campaign/{0}/".format(self.test_campaign.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Campaign.objects.count(), 1)
        self.assertEqual(Campaign.objects.get().target_product.id, self.test_product.id)


class CouponTests(APITestCase):
    def test_create_coupon(self):
        data = {'minimum_cart_amount': 100.00,
                'discount_rate': 10}

        response = self.client.post('/discounts/coupon/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coupon.objects.count(), 1)
        self.assertEqual(Coupon.objects.get().discount_rate, 10)

    def test_get_coupon(self):
        self.test_coupon = Coupon.objects.create(minimum_cart_amount=100.00, discount_rate=10)

        response = self.client.get("/discounts/coupon/{0}/".format(self.test_coupon.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Coupon.objects.count(), 1)
        self.assertEqual(Coupon.objects.get().discount_rate, 10)
