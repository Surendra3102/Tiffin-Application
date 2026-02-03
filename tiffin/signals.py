from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, Notification

@receiver(pre_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            message = f"Your order #{instance.id} status changed to: {instance.status}"
            Notification.objects.create(user=instance.user, message=message)
