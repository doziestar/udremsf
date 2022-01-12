"""
Signals for creating and updating users.

"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from udrems.users.models import (
    LandlordProfile,
    PropertyManagerProfile,
    TenantProfile,
    User,
)


@receiver(post_save, sender=User)
def create_and_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for a new user.
    """
    if created:
        if instance.account_type == "landlord":
            LandlordProfile.objects.create(user=instance)
        elif instance.account_type == "tenant":
            TenantProfile.objects.create(user=instance)
        elif instance.account_type == "property_managers":
            PropertyManagerProfile.objects.create(user=instance)


# update profile
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    """
    Update a profile for a user.
    """
    if instance.account_type == "landlord":
        instance.landlord.save()
    elif instance.account_type == "tenant":
        instance.tenant.save()
    elif instance.account_type == "property_managers":
        instance.property_manager.save()


# signal for switching account type and created profile
@receiver(pre_save, sender=User)
def create_profile_on_account_type_change(sender, instance, **kwargs):
    """
    Create a profile for a new user.
    """
    if instance.account_type == "landlord":
        if not instance.landlord_profile:
            LandlordProfile.objects.create(user=instance)
    elif instance.account_type == "tenant":
        if not instance.tenant_profile:
            TenantProfile.objects.create(user=instance)
    elif instance.account_type == "property_manager":
        if not instance.property_manager_profile:
            PropertyManagerProfile.objects.create(user=instance)
