from django.contrib.auth.models import User, Group
from .models import Blimp, Service
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('__all__')

class BlimpSerializer(serializers.ModelSerializer):
    #service_set = ServiceSerializer()
    class Meta:
        model = Blimp
        fields = ('domain', 'service_set')
        depth = 1
