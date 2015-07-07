from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Blimp

# Serializers define the API representation.

class BlimpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blimp
        fields = ('domain', 'ready', 'signature')
        # TODO: implement user-detail view to enable
        # fields = ('domain', 'owner', 'ready', 'signature')

# used for rendering the Blimp's owner
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')
