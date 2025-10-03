from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.get_recommendations, name='recommend'),
    path('watchlist/', views.get_watchlist, name='watchlist'),
    path('watchlist/add/', views.add_to_watchlist, name='add_watchlist'),
]
