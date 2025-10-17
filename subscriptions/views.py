from django.utils import timezone
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import SubscriptionPlan, Subscription
from .serializers import SubscriptionPlanSerializer, MySubscriptionSerializer

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True).order_by('price', 'period_days')
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

class MySubscriptionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MySubscriptionSerializer

    def get(self, request):
        now = timezone.now()
        sub = Subscription.objects.filter(
            user=request.user, canceled_at__isnull=True, start_at__lte=now, end_at__gte=now
        ).first()
        if not sub:
            return Response({"active": False}, status=status.HTTP_200_OK)
        data = self.get_serializer(sub).data
        data["active"] = True
        return Response(data, status=status.HTTP_200_OK)

class CancelSubscriptionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        now = timezone.now()
        sub = Subscription.objects.filter(
            user=request.user, canceled_at__isnull=True, start_at__lte=now, end_at__gte=now
        ).first()
        if not sub:
            return Response({"detail": "No active subscription."}, status=status.HTTP_400_BAD_REQUEST)
        sub.canceled_at = now
        sub.save(update_fields=["canceled_at"])
        return Response({"detail": "Subscription canceled."}, status=status.HTTP_200_OK)
