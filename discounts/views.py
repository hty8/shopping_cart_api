from rest_framework import viewsets
from .models import Campaign, Coupon
from .serializers import CampaignSerializer, CouponSerializer


class CampaignViewSet(viewsets.ModelViewSet):

    queryset = Campaign.objects.all().order_by('id')
    serializer_class = CampaignSerializer


class CouponViewSet(viewsets.ModelViewSet):

    queryset = Coupon.objects.all().order_by('id')
    serializer_class = CouponSerializer
