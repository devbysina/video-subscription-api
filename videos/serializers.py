from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Video
        fields = (
            'id', 'owner', 'title', 'description', 'is_free',
            'file', 'duration_sec', 'is_active', 'published_at',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
