from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import ClientProfile, ModelProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'model':
            ModelProfile.objects.create(user=instance)
        elif instance.user_type == 'client':
            ClientProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'model':
        if hasattr(instance, 'model_profile'):
            instance.model_profile.save()
        else:
            ModelProfile.objects.create(user=instance)
    elif instance.user_type == 'client':
        if hasattr(instance, 'client_profile'):
            instance.client_profile.save()
        else:
            ClientProfile.objects.create(user=instance)