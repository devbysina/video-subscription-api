from rest_framework import serializers
from django.utils import timezone
from .models import SubscriptionPlan, Subscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'name', 'price', 'period_days', 'is_active', 'created_at', 'updated_at')
        read_only_fields = fields

class MySubscriptionSerializer(serializers.ModelSerializer):
    is_active_now = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'start_at', 'end_at', 'canceled_at', 'created_at', 'updated_at', 'is_active_now')
        read_only_fields = fields

    def get_is_active_now(self, obj):
        now = timezone.now()
        return (obj.canceled_at is None) and (obj.start_at <= now <= obj.end_at)
