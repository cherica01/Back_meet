import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Custom user manager for the User model."""
    
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular user with the given email, username, and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a superuser with the given email, username, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'administrator')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """Custom user model for Hackitech platform."""
    
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('model', 'Model'),
        ('administrator', 'Administrator'),  # Ajouté pour gérer les superusers
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[("Homme", "Homme"), ("Femme", "Femme"), ("Autre", "Autre")], blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # Ajouté pour éviter l'erreur dans Meta
    last_active = models.DateTimeField(null=True, blank=True)  # Ajouté pour update_last_active
    languages = models.JSONField(default=list, blank=True, null=True)  # Correction ajoutée
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    user_type = models.CharField(max_length=15, choices=ROLE_CHOICES, default="client")  # Correction du choix

    # Vérification email
    is_verified = models.BooleanField(default=False)

    # Security settings
    two_factor_enabled = models.BooleanField(_('two-factor authentication'), default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def update_last_active(self):
        """Update the last active timestamp."""
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])


class UserFollowing(models.Model):
    """Model to track user following relationships."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('user following')
        verbose_name_plural = _('user followings')
        unique_together = ('user', 'following_user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} follows {self.following_user.username}"


class UserSession(models.Model):
    """User session information for security tracking."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(_('session key'), max_length=40)
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('user agent'))
    device_type = models.CharField(_('device type'), max_length=20)
    location = models.CharField(_('location'), max_length=100, blank=True)
    started_at = models.DateTimeField(_('started at'), auto_now_add=True)
    last_activity = models.DateTimeField(_('last activity'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('user session')
        verbose_name_plural = _('user sessions')
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"Session for {self.user.username} from {self.ip_address}"
