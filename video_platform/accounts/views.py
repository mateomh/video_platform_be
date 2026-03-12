from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounts.serializers import UserSerializer


class ListUsers(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdminUser]


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
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdminUser]

  def get_object(self):
    user_id = self.kwargs['user_id']
    user = get_object_or_404(User.objects, id = user_id)

    return user
  
  def perform_destroy(self, instance):
    instance.delete()

    return instance


class UserToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    serialized_data = self.serializer_class(data=request.data, context={'request': request})

    serialized_data.is_valid(raise_exception=True)

    user = serialized_data.validated_data['user']
    token = Token.objects.get_or_create(user=user)[0]

    return Response({
      'user_name': user.username,
      'token': token.key
    })
  

class UserInfo(generics.RetrieveAPIView):
  serializer_class = UserSerializer
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user

