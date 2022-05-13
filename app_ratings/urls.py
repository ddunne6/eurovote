from django.urls import path
from .views import CreateRating, EditRating, MyRatings, AllRatings

urlpatterns = [
    path('rate/', CreateRating.as_view(), name='rate'),
    path('update_rate/<int:pk>/', EditRating.as_view(), name='edit_rating'),
    path('', MyRatings.as_view(), name='my_ratings'),
    path('results/', AllRatings.as_view(), name='all_ratings'),
]
