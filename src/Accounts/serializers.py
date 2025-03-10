from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password2', 'gender', 'nationality', 
            'age', 'profile_picture', 'city', 'country', 'languages', 'user_type'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError("Identifiants invalides.")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'gender', 'nationality', 'age', 'profile_picture', 'city', 'country', 'languages', 'user_type']
        read_only_fields = ['email']  # On peut rendre l'email en lecture seule si nécessaire

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance