from rest_framework import viewsets
from .models import Video
from .serializers import VideoSerializer
from .permissions import CanViewOrEditVideo
from subscriptions.utils import has_active_subscription

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [CanViewOrEditVideo]

    def get_queryset(self):
        qs = Video.objects.filter(is_active=True)
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return qs
        if has_active_subscription(user):
            return qs
        return qs.filter(is_free=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
