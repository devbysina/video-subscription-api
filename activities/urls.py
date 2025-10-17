from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViewLogView, RatingViewSet, CommentViewSet

router = DefaultRouter()
router.register('ratings', RatingViewSet, basename='rating')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('viewlogs/', ViewLogView.as_view(), name='viewlogs'),
    path('', include(router.urls)),
]
