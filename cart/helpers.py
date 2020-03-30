from .models import Cart, DeliveryCost
from discounts.helpers import CampaignHelper, CouponHelper


class DeliveryCostHelper:

    def __init__(self, cart_items):
        self.cart_items = cart_items
        self.calculator = False
        self.number_of_deliveries = 0
        self.number_of_products = 0
        self.cost = 0

    def calculate_delivery_cost(self):
        try:
            self.calculator = DeliveryCost.objects.get(status='Active')

            delivery_categories = []

            for cart_item in self.cart_items:
                self.number_of_products += 1
                if cart_item.item.category.id not in delivery_categories:
                    delivery_categories.append(cart_item.item.category.id)
                    self.number_of_deliveries += 1

                self.cost = (self.calculator.cost_per_delivery * self.number_of_deliveries) + \
                            (self.calculator.cost_per_product * self.number_of_products) + self.calculator.fixed_cost

            return self.cost
        except Exception as e:
            print('Error when trying to getting coupon_discounts {0}'.format(str(e)))
            return False


class CartHelper:

    def __init__(self, user):
        self.user = user
        self.cart_base_total_amount = 0
        self.cart_final_total_amount = 0
        self.campaign_discount_amounts = []
        self.campaign_discount_amount = 0
        self.coupon_discount_amount = 0
        self.delivery_cost = 0
        self.cart_items = []
        self.discounts = {}
        self.checkout_details = {'products': [], 'total': [], 'amount': []}

    def prepare_cart_for_checkout(self):
        self.cart_items = Cart.objects.filter(user=self.user)

        if not self.cart_items:
            return False

        self.calculate_cart_base_total_amount()
        self.get_delivery_cost()
        self.get_campaign_discounts()
        self.get_coupon_discounts()
        self.calculate_discount_amounts()
        self.get_total_amount_after_discounts()
        self.prepare_checkout_details()

        return self.checkout_details

    def get_delivery_cost(self):
        delivery_helper = DeliveryCostHelper(cart_items=self.cart_items)
        self.delivery_cost = delivery_helper.calculate_delivery_cost()

    def calculate_cart_base_total_amount(self):
        for cart_item in self.cart_items:
            self.cart_base_total_amount += cart_item.item.price * cart_item.quantity

    def get_coupon_discounts(self):
        coupon_helper = CouponHelper(cart_total_amount=self.cart_base_total_amount)
        self.discounts['coupons'] = coupon_helper.get_coupon_discounts()

    def get_campaign_discounts(self):
        campaign_helper = CampaignHelper(self.cart_items)
        self.discounts['campaigns'] = campaign_helper.get_campaign_discounts()

    def calculate_discount_amounts(self):

        try:
            for discount in self.discounts.get('campaigns', []):
                if discount.discount_type == 'Amount':
                    self.campaign_discount_amounts.append(discount.amount.get('amount'))

                if discount.discount_type == 'Rate':
                    self.campaign_discount_amounts.append((self.cart_base_total_amount *
                                                           discount.amount.get('rate')) / 100)

            for discount in self.discounts.get('coupons', []):
                self.coupon_discount_amount = (self.cart_base_total_amount * discount.amount.get('rate')) / 100
        except Exception as e:
            print('Error when trying to calculating discount amounts {0}'.format(str(e)))

    def get_total_amount_after_discounts(self):

        if len(self.campaign_discount_amounts) > 0:
            self.campaign_discount_amount = max(self.campaign_discount_amounts)

        self.cart_final_total_amount = self.cart_base_total_amount - (
                    self.campaign_discount_amount + self.coupon_discount_amount)

        return self.cart_final_total_amount

    def prepare_checkout_details(self):
        for cart_item in self.cart_items:
            self.checkout_details['products'].append({'category_id': cart_item.item.category.id,
                                                      'category_name': cart_item.item.category.title,
                                                      'product_id': cart_item.item.id,
                                                      'product_name': cart_item.item.title,
                                                      'quantity': cart_item.quantity,
                                                      'unit_price': cart_item.item.price})

        self.checkout_details['total'].append({'total_price': self.cart_base_total_amount,
                                               'total_discount':
                                                   self.campaign_discount_amount + self.coupon_discount_amount})

        self.checkout_details['amount'].append({'total_amount': self.cart_final_total_amount,
                                                'delivery_cost': self.delivery_cost})
