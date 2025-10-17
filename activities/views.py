from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import ViewLog, Rating, Comment
from .serializers import (
    ViewLogSerializer, ViewLogCreateSerializer,
    RatingSerializer, CommentSerializer
)

class ViewLogView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ViewLog.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ViewLogCreateSerializer
        return ViewLogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Rating.objects.filter(user=self.request.user).order_by('-created_at')
        video_id = self.request.query_params.get('video')
        if video_id:
            qs = qs.filter(video_id=video_id)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        video = serializer.validated_data.get('video')
        score = serializer.validated_data.get('score')


        obj, created = Rating.objects.update_or_create(
            user=user, video=video,
            defaults={'score': score}
        )
        out = self.get_serializer(obj)
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Comment.objects.filter(user=self.request.user).order_by("created_at")
        video_id = self.request.query_params.get("video")
        if video_id:
            qs = qs.filter(video_id=video_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
