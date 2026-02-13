from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from accounts.serializers import UserSerializer


class ListUsers(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
  serializer_class = UserSerializer

  def get_object(self):
    user_id = self.kwargs['user_id']
    user = get_object_or_404(User.objects, id = user_id)

    return user


class RegisterUser(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class DeleteUser(generics.DestroyAPIView):
  serializer_class = UserSerializer

  def get_object(self):
    user_id = self.kwargs['user_id']
    user = get_object_or_404(User.objects, id = user_id)

    return user
  
  def perform_destroy(self, instance):
    instance.delete()

    return instance
