from django.db import models
from django.conf import settings
from accounts.models import User

class ModelProfile(models.Model):
    """Profil spécifique pour les utilisateurs de type 'model'"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='model_profile')
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    tokens_per_minute = models.PositiveIntegerField(default=5)
    specialties = models.ManyToManyField('Specialty', blank=True)
    availability = models.TextField(blank=True)
    experience = models.CharField(max_length=50, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_calls = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    verification_documents = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Model Profile: {self.user.username}"

class ClientProfile(models.Model):
    """Profil spécifique pour les utilisateurs de type 'client'"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    bio = models.TextField(blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    favorite_categories = models.ManyToManyField('Category', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client Profile: {self.user.username}"

class Specialty(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Specialties"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='profile_photos/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.user.username}"