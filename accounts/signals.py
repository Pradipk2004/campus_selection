from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile, RecruiterProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile after user is created."""
    if not created:
        return

    # Skip admin/staff
    if instance.is_superuser or instance.is_staff:
        return

    if instance.role == CustomUser.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)
    elif instance.role == CustomUser.RECRUITER:
        RecruiterProfile.objects.get_or_create(user=instance)
