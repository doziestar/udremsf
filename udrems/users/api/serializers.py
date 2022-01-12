from django.contrib.auth import get_user_model
from rest_framework import serializers

from udrems.users.models import LandlordProfile, PropertyManagerProfile, TenantProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = ["url", "landlord_profile"]

        extra_kwargs = {
            "url": {
                "view_name": "api:landlord-detail",
                "lookup_field": "user__username",
            }
        }


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ["url", "tenant_profile"]

        extra_kwargs = {
            "url": {"view_name": "api:tenant-detail", "lookup_field": "user__username"}
        }


class PropertyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyManagerProfile
        fields = ["url", "property_manager_profile"]

        extra_kwargs = {
            "url": {
                "view_name": "api:property_manager-detail",
                "lookup_field": "user__username",
            }
        }
