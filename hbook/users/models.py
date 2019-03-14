"""
 Lol Happens
"""
from django.db import models
from django.contrib.auth.models import User as Usr
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    For user serializer
    """
    class Meta:
        model = Usr
        fields = ('url', 'email', 'username', 'groups', 'details')

class User2(models.Model):
    """User Details
    Providing extra fields to default user model
    """
    name = models.CharField(max_length=30)
    auth = models.OneToOneField(Usr, related_name='details', on_delete=models.CASCADE)
    info = models.TextField(default='{}')

    def __str__(self):
        return str(self.pk)+" "+ self.name

class User2Serializer(serializers.HyperlinkedModelSerializer):
    """
    User serilizer
    """
    class Meta:
        model = User2
        fields = ('url', 'name', 'auth', 'info')

