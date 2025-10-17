from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, MySubscriptionView, CancelSubscriptionView

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plan')

urlpatterns = [
    path('', include(router.urls)),
    path('my/', MySubscriptionView.as_view(), name='my_subscription'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
]
