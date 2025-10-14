from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period_days = models.PositiveIntegerField(default=30)
    is_recurring = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.period_days}d)'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    canceled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_active_now(self):
        now = timezone.now()
        return (self.canceled_at is None) and (self.start_at <= now <= self.end_at)

    def __str__(self):
        return f'{self.user} [{self.start_at:%Y-%m-%d} → {self.end_at:%Y-%m-%d}]'
