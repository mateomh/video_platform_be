from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import ListUsers, UserDetail, RegisterUser, DeleteUser

app_name = 'accounts'

urlpatterns = [
  path('register/', RegisterUser.as_view(), name = 'register'),
  path('user/', ListUsers.as_view(), name = 'list'),
  path('user/<int:user_id>', UserDetail.as_view(), name = 'detail'),
  path('user/<int:user_id>/delete', DeleteUser.as_view(), name = 'delete'),
]