from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Video(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='videos',
        limit_choices_to={'is_staff': True},
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_free = models.BooleanField(default=True)
    file = models.FileField(upload_to='videos/')
    duration_sec = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
