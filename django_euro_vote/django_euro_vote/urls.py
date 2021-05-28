from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('app_users.urls')),
    path('admin/', admin.site.urls),
    path('', include('app_ratings.urls')),
]
