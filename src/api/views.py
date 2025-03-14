from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import User, UserFollowing
from profiles.models import Photo
from api.serializers import (UserSerializer, UserFollowingSerializer, 
                                  UserFollowersSerializer, PhotoSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_verified', 'gender', 'city', 'country']
    search_fields = ['username', 'first_name', 'last_name', 'city', 'country']
    ordering_fields = ['registration_date', 'followers_count', 'views_count']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def models(self, request):
        models = User.objects.filter(user_type='model')
        page = self.paginate_queryset(models)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(models, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = UserFollowing.objects.filter(user=user)
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = UserFollowingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserFollowingSerializer(following, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = UserFollowing.objects.filter(following_user=user)
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = UserFollowersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserFollowersSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        
        if user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        following, created = UserFollowing.objects.get_or_create(
            user=user, following_user=user_to_follow
        )
        
        if created:
            user_to_follow.followers_count += 1
            user_to_follow.save()
            user.following_count += 1
            user.save()
            return Response({"detail": f"You are now following {user_to_follow.username}."}, 
                           status=status.HTTP_201_CREATED)
        
        return Response({"detail": f"You are already following {user_to_follow.username}."}, 
                       status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        user = request.user
        
        try:
            following = UserFollowing.objects.get(
                user=user, following_user=user_to_unfollow
            )
            following.delete()
            
            user_to_unfollow.followers_count -= 1
            user_to_unfollow.save()
            user.following_count -= 1
            user.save()
            
            return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, 
                           status=status.HTTP_200_OK)
        except UserFollowing.DoesNotExist:
            return Response({"detail": f"You are not following {user_to_unfollow.username}."}, 
                           status=status.HTTP_400_BAD_REQUEST)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)