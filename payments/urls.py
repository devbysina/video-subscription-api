from django.urls import path
from .views import MyPaymentsListView, PaymentCreateView

urlpatterns = [
    path('my/', MyPaymentsListView.as_view(), name='my_payments'),
    path('',  PaymentCreateView.as_view(),    name='create_payment')
]
