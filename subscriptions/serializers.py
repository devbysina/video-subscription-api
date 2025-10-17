from rest_framework import serializers
from .models import SubscriptionPlan, Subscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'name', 'price', 'period_days', 'is_active', 'created_at', 'updated_at')
        read_only_fields = fields

class MySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'start_at', 'end_at', 'canceled_at', 'created_at', 'updated_at')
        read_only_fields = fields
