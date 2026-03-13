from django.urls import path
from accounts.views import ListUsers, UserDetail, RegisterUser, DeleteUser, UserToken, UserInfo

app_name = 'accounts'

urlpatterns = [
  path('register/', RegisterUser.as_view(), name = 'register'),
  path('token/', UserToken.as_view(), name = 'token'),
  path('user/', ListUsers.as_view(), name = 'list'),
  path('user/<int:user_id>', UserDetail.as_view(), name = 'detail'),
  path('user/<int:user_id>/delete', DeleteUser.as_view(), name = 'delete'),
  path('me', UserInfo.as_view(), name = 'me'),
]