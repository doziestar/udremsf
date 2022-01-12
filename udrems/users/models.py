from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for udrems."""

    ACCOUNT_TYPE = (
        ("landlord", "Landlord"),
        ("tenant", "Tenants"),
        ("property_manager", "Property Managers"),
        ("staff", "Staffs"),
    )
    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    account_type = models.CharField(
        choices=ACCOUNT_TYPE, default="tenant", max_length=20
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) -> str:
        return self.username


# profile for users
class Profile(models.Model):
    """
    Profile account for users. User can have different types of account
    account_type:
    1. Landlord
    2. Tenants
    3. Property Managers
    4. Staff

    """

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics", blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    # get full address
    def get_full_address(self) -> str:
        return f"{self.address}, {self.city}, {self.state}, {self.zip_code}, {self.country}"

    # change account type
    def change_account_type(self, account_type: int) -> None:
        self.account_type = account_type
        self.save()

    # def __str__(self):
    #     return self.user.username

    class Meta:
        abstract = True


# landlord profile
class LandlordProfile(Profile):
    """
    Profile account for Landlords.
    1. Can have many tenants
    2. Can have many property managers
    3. Can have many staffs
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    property_managers = models.ManyToManyField(
        "PropertyManager", related_name="property_managers"
    )
    tenants = models.ManyToManyField("Tenant", related_name="tenants")
    # staffs = models.ManyToManyField("users.Staff", related_name="staffs")


class TenantProfile(Profile):
    """
    Profile account for Tenants.
    1. Can have many landlords
    2. Can have many property managers
    3. Can have many staffs
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    landlords = models.ManyToManyField(LandlordProfile, related_name="landlords")
    property_managers = models.ManyToManyField(
        "PropertyManager", related_name="property_managers"
    )


class PropertyManagerProfile(Profile):
    """
    Profile account for Property Managers.
    1. Can have many landlords
    2. Can have many tenants
    3. Can have many staffs
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    landlords = models.ManyToManyField(LandlordProfile, related_name="landlords")
    tenants = models.ManyToManyField(TenantProfile, related_name="tenants")
    # staffs = models.ManyToManyField("users.Staff", related_name="staffs")
