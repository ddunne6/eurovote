from django.contrib import admin
from .models import (
    Country,
    Rating,
)

admin.site.register(Country)
admin.site.register(Rating)