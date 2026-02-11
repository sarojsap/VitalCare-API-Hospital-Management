from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Patient, Doctor

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Automatically create a profile when a User is created
    if created:
        if instance.role == User.RoleOption.PATIENT:
            Patient.objects.create(user=instance)

        elif instance.role == User.RoleOption.DOCTOR:
            Doctor.objects.create(user=instance)