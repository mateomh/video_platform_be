from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = '__all__'

  def create(self, validated_data):
    # Use the create_user method to ensure the password is hashed correctly
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
    )
    return user

