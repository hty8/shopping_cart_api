from .models import Campaign, Coupon
from rest_framework import serializers


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'discount_type', 'discount_rate', 'discount_amount', 'min_purchased_items',
                  'apply_to', 'target_product', 'target_category', 'created_at', 'updated_at']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'minimum_cart_amount', 'discount_rate', 'created_at', 'updated_at']