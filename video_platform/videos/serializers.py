from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video

class VideoOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class VideoSerializer(serializers.ModelSerializer):
    user = VideoOwnerSerializer(read_only=True)

    class Meta:
        model = Video
        fields = '__all__'

