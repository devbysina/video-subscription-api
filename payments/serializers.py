from rest_framework import serializers
from .models import Payment
from subscriptions.models import SubscriptionPlan

class PaymentCreateSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate(self, attrs):
        plan_id = attrs['plan_id']
        try:
            plan = SubscriptionPlan.objects.get(pk=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError({"plan_id": "Invalid or inactive plan."})
        attrs['plan'] = plan
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    plan = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'plan', 'amount', 'created_at')
        read_only_fields = ('id', 'plan', 'amount', 'created_at')
