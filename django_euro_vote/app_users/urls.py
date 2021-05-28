from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app_users/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
