import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

class UserType(models.TextChoices):
    CLIENT = "Client", "Client"
    MODEL = "Model", "Model"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[("Homme", "Homme"), ("Femme", "Femme"), ("Autre", "Autre")], blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    languages = models.JSONField(default=list)  # Liste des langues parlées
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CLIENT)

    # Vérification email
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, default=generate_verification_code)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
