from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def make_owner_admin(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.email == settings.OWNER_EMAIL:
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
