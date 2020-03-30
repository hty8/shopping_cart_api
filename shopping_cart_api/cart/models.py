from django.db import models
from shopping_cart_api.products.models import Product


class User(models.Model):
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}".format(self.name,
                                     self.created_at,
                                     self.updated_at)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.item,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)


class DeliveryCost(models.Model):
    status = models.CharField(max_length=7,
                              choices=(('Active', 'active'), ('Passive', 'passive')),
                              default="passive",
                              null=False)
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.status,
                                                    self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)
