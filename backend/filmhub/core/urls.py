from django.urls import path
from .views import RegisterView, LoginView, LogoutView, get_movie_by_id, add_to_watchlist, get_watchlist, delete_from_watchlist, add_favorite, get_favorites, delete_favorite, set_preference, get_user_preferences, delete_user_preferences, add_WatchedHistory, get_WatchedHistory, delete_WatchedHistory, MoviesWithDetailsView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('movies/popular/', MoviesWithDetailsView.as_view(), name='popular-movies'),
    path('movies/search/<int:movie_id>/', get_movie_by_id, name='search-movies'),

    path('watchlist/', add_to_watchlist, name='add-watchlist'),
    path('watchlist/all/', get_watchlist, name='get-watchlist'),
    path('watchlist/<str:movie_id>/', delete_from_watchlist, name='delete-watchlist'),

    path('favorites/', add_favorite, name='add-favorite'),
    path('favorites/all/', get_favorites, name='get-favorites'),
    path('favorites/<str:movie_id>/', delete_favorite, name='delete-favorite'),

    path('watchedhistory', add_WatchedHistory, name='add_watchedhistory'),
    path('watchedhistory', get_WatchedHistory, name='get_watchedhistory'),
    path('watchedhistory', delete_WatchedHistory, name='delete_watchedhistory'),

    path('preference', set_preference, name='add_preference'),
    path('preferences', get_user_preferences, name='get_preference'),
    path('preferences', delete_user_preferences, name='delete_preferences'),
    

]
