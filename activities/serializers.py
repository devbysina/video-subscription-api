from rest_framework import serializers
from .models import ViewLog, Rating, Comment
from subscriptions.utils import has_active_subscription

def _ensure_can_view_video(user, video):
    if video.is_free:
        return
    if not has_active_subscription(user):
        raise serializers.ValidationError("You do not have access to this video.")

def _ensure_has_watched(user, video):
    exists = ViewLog.objects.filter(user=user, video=video).exists()
    if not exists:
        raise serializers.ValidationError("You must watch the video before rating or commenting.")


class ViewLogSerializer(serializers.ModelSerializer):
    video = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ViewLog
        fields = ("id", "video", "created_at")
        read_only_fields = ("id", "video", "created_at")


class ViewLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewLog
        fields = ("id", "video", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        request = self.context["request"]
        _ensure_can_view_video(request.user, attrs["video"])
        return attrs


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "video", "score", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        video = attrs.get("video") or getattr(self.instance, "video", None)
        if video is None:
            raise serializers.ValidationError({"video": "Video is required."})
        _ensure_has_watched(request.user, video)
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "video", "body", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        video = attrs.get("video") or getattr(self.instance, "video", None)
        if video is None:
            raise serializers.ValidationError({"video": "Video is required."})
        _ensure_has_watched(request.user, video)
        return attrs
