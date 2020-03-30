from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, null=False)
    parent_category_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.title,
                                          self.parent_category_id,
                                          self.created_at,
                                          self.updated_at)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.category,
                                               self.title,
                                               self.price,
                                               self.created_at,
                                               self.updated_at)
