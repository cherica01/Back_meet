from rest_framework import serializers
from accounts.models import User, UserFollowing, UserSession
from profiles.models import ModelProfile, ClientProfile, Photo

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id', 'ip_address', 'device_type', 'location', 'started_at', 'last_activity', 'is_active']

class UserFollowingSerializer(serializers.ModelSerializer):
    following_username = serializers.CharField(source='following_user.username', read_only=True)
    following_profile_picture = serializers.ImageField(source='following_user.profile_picture', read_only=True)
    
    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user', 'following_username', 'following_profile_picture', 'created_at']

class UserFollowersSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='user.username', read_only=True)
    follower_profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    
    class Meta:
        model = UserFollowing
        fields = ['id', 'user', 'follower_username', 'follower_profile_picture', 'created_at']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'is_primary', 'caption', 'uploaded_at']

class ModelProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelProfile
        fields = ['bio', 'hourly_rate', 'tokens_per_minute', 'specialties', 
                  'availability', 'experience', 'rating', 'total_calls', 'is_featured']

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['bio', 'preferences', 'favorite_categories']

class UserSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    model_profile = ModelProfileSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'gender', 
                  'nationality', 'age', 'profile_picture', 'city', 'country', 
                  'languages', 'followers_count', 'following_count', 'like_count', 
                  'views_count', 'user_type', 'is_verified', 'last_active', 
                  'photos', 'model_profile', 'client_profile']
        read_only_fields = ['id', 'followers_count', 'following_count', 'like_count', 
                           'views_count', 'is_verified', 'last_active']