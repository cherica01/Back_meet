from django.db import models
from accounts.models import User

# Nous pouvons utiliser le modèle UserFollowing existant pour les favoris utilisateurs
# et créer un modèle supplémentaire pour les autres types de favoris

class Bookmark(models.Model):
    CONTENT_TYPES = (
        ('event', 'Event'),
        ('video', 'Video'),
        ('live', 'Live Stream'),
        ('post', 'Post'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_content')
    thumbnail = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.content_type}: {self.title}"