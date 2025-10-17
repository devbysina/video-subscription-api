from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

router = DefaultRouter()
router.register('', VideoViewSet, basename='video')

urlpatterns = router.urls
