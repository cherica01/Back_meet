from django.db import models
from accounts.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(blank=True)
    media_url = models.URLField(blank=True)
    media_type = models.CharField(max_length=20, blank=True)
    caption = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='sent')  # sent, delivered, read
    reactions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation.id}"
    
    class Meta:
        ordering = ['created_at']