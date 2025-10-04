from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.conf import settings
import requests
from rest_framework.decorators import api_view, permission_classes
from .models import Watchlist, Favorite, WatchedHistory, UserPreference, Recommendation
from .serializers import WatchlistSerializer, FavoriteSerializer, WatchedHistorySerializer, UserPreferenceSerializer, RecommendationSerializer

class RegisterView(APIView):
    """
    API endpoint to register a new user.

    Method: POST
    URL: /register/

    Expected request data (JSON):
    {
        "username": "your_username",
        "email": "your_email@example.com",
        "password": "your_password",
        "confirm_password": "your_password"
    }

    Responses:
    - 201 Created: User registered successfully
    - 400 Bad Request: Validation errors
    """
    
    def post(self, request):
        """
        Handles POST requests to register a user.
        Uses RegisterSerializer to validate input and save user to database.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    """
    API endpoint to login a user using JWT.

    Method: POST
    URL: /login/

    Expected request data (JSON):
    {
        "username": "your_username",
        "password": "your_password"
    }

    Responses:
    - 200 OK: Returns access and refresh JWT tokens
    - 401 Unauthorized: Invalid credentials
    """
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class PopularMoviesView(APIView):
#     """
#     API endpoint to fetch popular movies from TMDb.

#     Method: GET
#     URL: /movies/popular/
#     """
#     def get(self, request):
#         try:
#             url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"
#             headers = {
#                 "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}",
#                 "Content-Type": "application/json;charset=utf-8"
#             }
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             data = response.json()
#             return Response(data, status=status.HTTP_200_OK)
#         except requests.exceptions.RequestException as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#! ------------------watchlist endpoints------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):
    """
    Add a movie to the user's watchlist.
    Request body:
    {
        "movie_id": "123",
        "status": "to_watch"  # optional, default to 'to_watch'
    }
    """
    movie_id = request.data.get('movie_id')
    status_choice = request.data.get('status', 'to_watch')

    if not movie_id:
        return Response({"error": "movie_id is required"}, status=400)

    watch_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        movie_id=movie_id,
        defaults={'status': status_choice}
    )

    if not created:
        watch_item.status = status_choice
        watch_item.save()

    serializer = WatchlistSerializer(watch_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    """
    Get all movies in the user's watchlist.
    """
    watchlist = Watchlist.objects.filter(user=request.user)
    serializer = WatchlistSerializer(watchlist, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_watchlist(request, movie_id):
    """
    Delete a movie from the user's watchlist by movie_id
    """
    try:
        watch_item = Watchlist.objects.get(user=request.user, movie_id=movie_id)
        watch_item.delete()
        return Response({"message": "Movie removed from watchlist"}, status=status.HTTP_200_OK)
    except Watchlist.DoesNotExist:
        return Response({"error": "Movie not found in watchlist"}, status=status.HTTP_404_NOT_FOUND)

#! ------------------Favorite endpoints------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    """
    Add a movie to the user's favorites.
    Request body:
    {
        "movie_id": "123"
    }
    """
    movie_id = request.data.get('movie_id')
    if not movie_id:
        return Response({"error": "movie_id is required"}, status=400)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        movie_id=movie_id
    )

    serializer = FavoriteSerializer(favorite)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    """
    Get all movies in the user's favorites.
    """
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request, movie_id):
    """
    Delete a movie from the user's favorites by movie_id.
    """
    try:
        favorite = Favorite.objects.get(user=request.user, movie_id=movie_id)
        favorite.delete()
        return Response({"message": "Movie removed from favorites"}, status=status.HTTP_200_OK)
    except Favorite.DoesNotExist:
        return Response({"error": "Movie not found in favorites"}, status=status.HTTP_404_NOT_FOUND)

#! ------------------WatchedHistory endpoints------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_WatchedHistory(request):
    """
    Add a movie to the user's watched history.
    Request body:
    {
        "movie_id": "123"
    }
    """
    movie_id = request.data.get('movie_id')
    if not movie_id:
        return Response({"error": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    watchedhistory, created = WatchedHistory.objects.get_or_create(
        user=request.user,
        movie_id=movie_id,
    )

    serializer = WatchedHistorySerializer(watchedhistory)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ✅ Get
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_WatchedHistory(request):
    """
    Get all movies in the user's watched history.
    """
    watchedhistory = WatchedHistory.objects.filter(user=request.user)
    serializer = WatchedHistorySerializer(watchedhistory, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_WatchedHistory(request, movie_id):
    """
    Delete a movie from the user's watched history by movie_id.
    """
    try:
        watchedhistory = WatchedHistory.objects.get(user=request.user, movie_id=movie_id)
        watchedhistory.delete()
        return Response({"message": "Movie removed from WatchedHistory"}, status=status.HTTP_200_OK)
    except WatchedHistory.DoesNotExist:
        return Response({"error": "Movie not found in WatchedHistory"}, status=status.HTTP_404_NOT_FOUND)
#! ------------------preference endpoints------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_preference(request):
    """
    Set or update liked/disliked for a specific movie.
    liked and disliked are mutually exclusive.
    Request body:
    {
        "movie_id": "<movie id>",
        "liked": true/false,
        "disliked": true/false
    }
    """
    movie_id = request.data.get('movie_id')
    if not movie_id:
        return Response({"error": "movie_id is required"}, status=400)

    liked = request.data.get('liked', False)
    disliked = request.data.get('disliked', False)

    if liked:
        disliked = False
    elif disliked:
        liked = False

    pref, _ = UserPreference.objects.get_or_create(user=request.user, movie_id=movie_id)
    pref.liked = liked
    pref.disliked = disliked
    pref.save()

    return Response({
        "message": "Preferences updated",
        "movie_id": movie_id,
        "liked": pref.liked,
        "disliked": pref.disliked
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_preferences(request):
    """
    Retrieve the current user's preferences.
    """
    try:
        pref = UserPreference.objects.get(user=request.user)
        serializer = UserPreferenceSerializer(pref)
        return Response(serializer.data)
    except UserPreference.DoesNotExist:
        return Response({"error": "Preferences not found"}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_preferences(request):
    """
    Delete the current user's preferences.
    """
    try:
        pref = UserPreference.objects.get(user=request.user)
        pref.delete()
        return Response({"message": "Preferences deleted successfully"})
    except UserPreference.DoesNotExist:
        return Response({"error": "Preferences not found"}, status=404)

#! ------------------ endpoints------------------

@api_view(['GET'])
def get_movie_by_id(request, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}"
    headers = {
        "Authorization": f"Bearer {settings.TMDB_READ_ACCESS_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({"error": "Movie not found"}, status=response.status_code)




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_gemini_recommendations(request):
#     user = request.user
    
#     liked_movies = list(Favorite.objects.filter(user=user).values_list('movie_id', flat=True))
#     disliked_movies = list(UserPreference.objects.filter(user=user, disliked=True).values_list('movie_id', flat=True))
#     watchlist_movies = list(Watchlist.objects.filter(user=user).values_list('movie_id', flat=True))
    
#     prompt = f"""
#     User likes these movies: {liked_movies}
#     User dislikes these movies: {disliked_movies}
#     User watchlist: {watchlist_movies}
    
#     Suggest 5 movies this user will likely enjoy.
#     """
    
#     headers = {
#         "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     response = requests.post(
#         settings.GEMINI_API_URL,
#         json={"prompt": prompt, "max_results": 5},
#         headers=headers
#     )
    
#     if response.status_code != 200:
#         return Response({"error": "Gemini API request failed"}, status=response.status_code)
    
#     recommendations = response.json().get("recommendations", [])
    
#     # Save & serialize
#     saved_recommendations = []
#     for movie_id in recommendations:
#         rec, created = Recommendation.objects.get_or_create(user=user, movie_id=movie_id)
#         saved_recommendations.append(rec)

#     serializer = RecommendationSerializer(saved_recommendations, many=True)
#     return Response(serializer.data)




import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MoviesWithDetailsView(APIView):
    """
    API endpoint to fetch 50 movies (popular) with full details including cast, trailer, etc.
    Method: GET
    URL: /movies/popular-detailed/
    """

    def get(self, request):
        try:
            # Step 1: Get popular movies (first 3 pages = ~60 movies)
            movies = []
            for page in range(1, 4):  # fetch 3 pages (20 each)
                url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page={page}"
                response = requests.get(url)
                response.raise_for_status()
                movies.extend(response.json().get("results", []))

            detailed_movies = []

            # Step 2: For each movie, fetch details, credits, and trailers
            for movie in movies[:50]:  # limit to 50
                movie_id = movie["id"]

                # Movie details
                details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=en-US"
                details = requests.get(details_url).json()

                # Credits (cast)
                credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={settings.TMDB_API_KEY}&language=en-US"
                credits = requests.get(credits_url).json()
                cast = [
                    {
                        "id": c["id"],
                        "name": c["name"],
                        "character": c.get("character"),
                        "image": f"https://image.tmdb.org/t/p/w200{c['profile_path']}" if c.get("profile_path") else None
                    }
                    for c in credits.get("cast", [])[:5]  # top 5 cast members
                ]

                # Videos (trailers)
                videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={settings.TMDB_API_KEY}&language=en-US"
                videos = requests.get(videos_url).json()
                trailer = None
                for v in videos.get("results", []):
                    if v["site"] == "YouTube" and v["type"] == "Trailer":
                        trailer = f"https://www.youtube.com/embed/{v['key']}"
                        break

                # Step 3: Format JSON response
                detailed_movies.append({
                    "id": details["id"],
                    "title": details["title"],
                    "releaseDate": details.get("release_date"),
                    "rating": details.get("vote_average"),
                    "runtime": details.get("runtime"),
                    "genres": [g["name"] for g in details.get("genres", [])],
                    "overview": details.get("overview"),
                    "poster": f"https://image.tmdb.org/t/p/w500{details['poster_path']}" if details.get("poster_path") else None,
                    "backdrop": f"https://image.tmdb.org/t/p/original{details['backdrop_path']}" if details.get("backdrop_path") else None,
                    "trailer": trailer,
                    "cast": cast
                })

            return Response(detailed_movies, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
