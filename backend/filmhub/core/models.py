from django.db import models
from django.contrib.auth.models import User

# 1. Watchlist
class Watchlist(models.Model):
    STATUS_CHOICES = [
        ('to_watch', 'To Watch'),
        ('watching', 'Watching'),
        ('completed', 'Completed')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=50)  # from external API
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_watch')

    def __str__(self):
        return f"{self.user.username} - {self.movie_id} ({self.status})"

# 2. Favorites
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_id}"

# 3. Watched History
class WatchedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_rating = models.PositiveIntegerField(null=True, blank=True)
    user_review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} watched {self.movie_id}"

# 4. User Preferences
class UserPreference(models.Model):
    CONTENT_CHOICES = [
        ('Movies', 'Movies'),
        ('TV Shows', 'TV Shows'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_genres = models.CharField(max_length=200)
    disliked_genres = models.CharField(max_length=200)
    liked_actors = models.CharField(max_length=200, null=True, blank=True)
    disliked_actors = models.CharField(max_length=200, null=True, blank=True)
    preferred_age_rating = models.CharField(max_length=10)
    preferred_content_type = models.CharField(max_length=20, choices=CONTENT_CHOICES, default='Movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

# 5. Recommendations
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=50)  # e.g., GeminiAI, System
    context = models.CharField(max_length=200, null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.movie_id}"

# 6. User Queries
class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    response_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Query by {self.user.username} at {self.created_at}"
