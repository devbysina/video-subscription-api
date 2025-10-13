from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import SubscriptionPlan, Subscription

User = get_user_model()

class Payment(models.Model):
    STATUS_CHOICES = (
        ('initiated', 'Initiated'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='payments')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.plan} - {self.status} - {self.amount}'

    def mark_paid_and_apply(self):
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])

        now = timezone.now()

        active = Subscription.objects.filter(
            user=self.user,
            status='active',
            start_at__lte=now,
            end_at__gte=now,
        ).order_by('-end_at').first()

        if active:
            active.end_at = active.end_at + timedelta(days=self.plan.period_days)
            active.save(update_fields=['end_at'])
            return active

        return Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_at=now,
            end_at=now + timedelta(days=self.plan.period_days),
            status='active',
        )
