from rest_framework import serializers

from .models import Invite


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'
        lookup_field = 'slug'
