from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from subscriptions.models import SubscriptionPlan, Subscription

User = get_user_model()

RENEW_WINDOW_DAYS = 30

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='payments')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.plan} - {self.amount}'

    def apply_subscription(self):
        now = timezone.now()
        active = Subscription.objects.filter(
            user=self.user,
            canceled_at__isnull=True,
            start_at__lte=now,
            end_at__gte=now,
        ).first()

        if active is None:
            return Subscription.objects.create(
                user=self.user,
                start_at=now,
                end_at=now + timedelta(days=self.plan.period_days),
            )

        days_left = (active.end_at.date() - now.date()).days
        if days_left > RENEW_WINDOW_DAYS:
            raise ValidationError(
                f"Renewal not allowed yet. Days left: {days_left}, window: {RENEW_WINDOW_DAYS}"
            )

        active.end_at = active.end_at + timedelta(days=self.plan.period_days)
        active.save(update_fields=['end_at'])
        return active
