from django.utils import timezone
from .models import Subscription

def has_active_subscription(user):
    if not (user and user.is_authenticated):
        return False
    now = timezone.now()
    return Subscription.objects.filter(
        user=user,
        canceled_at__isnull=True,
        start_at__lte=now,
        end_at__gte=now,
    ).exists()
