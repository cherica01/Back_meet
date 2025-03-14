# accounts/serializers.py
from rest_framework import serializers

from .models import User, UserFollowing, UserSession
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'gender', 
            'nationality', 'age', 'profile_picture', 'city', 'country', 
            'languages', 'followers_count', 'following_count', 'like_count', 
            'views_count', 'user_type', 'is_verified', 'two_factor_enabled', 
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'followers_count', 'following_count', 'like_count', 
                            'views_count', 'is_verified', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Créer un utilisateur avec un mot de passe sécurisé"""
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """Mettre à jour l'utilisateur en gérant le mot de passe correctement"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance



class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id', 'session_key', 'ip_address', 'user_agent', 'device_type', 
                  'location', 'started_at', 'last_activity', 'is_active']
        read_only_fields = ['id', 'user', 'started_at', 'last_activity']


class UserFollowingSerializer(serializers.ModelSerializer):
    following_user_details = UserSerializer(source='following_user', read_only=True)
    
    class Meta:
        model = UserFollowing
        fields = ['id', 'following_user', 'following_user_details', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class InitiateRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class CompleteRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()]
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )