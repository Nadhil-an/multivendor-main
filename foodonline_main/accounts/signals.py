from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new User is created.
    Update profile if it exists.
    """
    # get_or_create ensures we never create duplicates
    profile, created_profile = UserProfile.objects.get_or_create(
        user=instance,
        defaults={'name': f"{instance.first_name} {instance.last_name}".strip()}
    )
    if not created_profile:
        # Optionally update the name in case first/last name changed
        profile.name = f"{instance.first_name} {instance.last_name}".strip()
        profile.save()


@receiver(pre_save, sender=User)
def pre_save(sender, instance, **kwargs):
    print(f"{instance.username} is being saved")
