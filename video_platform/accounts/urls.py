from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView

app_name = 'accounts'

urlpatterns = [
  path('register/', RegisterView.as_view(), name = 'register'),
  path('login/', auth_views.LoginView.as_view(
    template_name = 'accounts/login.html',
    redirect_authenticated_user = True
  ), name = 'login'),
  path('logout/', auth_views.LogoutView.as_view(
    template_name = 'accounts/logout.html'
  ), name = 'logout')
]