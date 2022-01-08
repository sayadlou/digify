from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from .tasks import notify_customers


@receiver(post_save, sender=Transaction)
def create_profile(sender, instance, created, **kwargs):
    if created:
        sms = {
            'content': f'{instance.type} for {instance.id}',
            'mobile_number': instance.account.owner.mobile_number,
        }
        notify_customers.delay(sms)
