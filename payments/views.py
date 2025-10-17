from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentSerializer

class MyPaymentsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')

class PaymentCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentCreateSerializer

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        plan = ser.validated_data['plan']

        with transaction.atomic():
            payment = Payment.objects.create(
                user=request.user,
                plan=plan,
                amount=plan.price
            )
            try:
                sub = payment.apply_subscription()
            except ValidationError as e:
                return Response(
                    {"errors": e.messages if hasattr(e, 'messages') else [str(e)]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = PaymentSerializer(payment).data
        data['subscription_end_at'] = sub.end_at
        return Response(data, status=status.HTTP_201_CREATED)
