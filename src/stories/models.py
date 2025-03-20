from django.db import models
from accounts.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # 24 heures après created_at
    
    def __str__(self):
        return f"Story by {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Stories"

class StoryItem(models.Model):
    ITEM_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=10, choices=ITEM_TYPES)
    url = models.URLField()
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.type} in story by {self.story.user.username}"

class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_stories')
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'user')
    
    def __str__(self):
        return f"{self.user.username} viewed {self.story.user.username}'s story"