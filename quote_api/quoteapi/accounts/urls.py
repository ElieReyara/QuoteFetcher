from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.forms import CustomLoginForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',
        authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]