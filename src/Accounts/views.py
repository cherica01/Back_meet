# accounts/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, UserFollowing, UserSession
from .permissions import IsOwnerOrReadOnly, IsUserOrAdmin
from .serializers import (UserFollowingSerializer, UserProfileSerializer,
                          UserSerializer, UserSessionSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']
    ordering_fields = ['username', 'date_joined', 'points']
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        following, created = UserFollowing.objects.get_or_create(
            user=request.user,
            following_user=user
        )
        
        if created:
            return Response(
                {"detail": f"You are now following {user.username}."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": f"You are already following {user.username}."}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        try:
            following = UserFollowing.objects.get(
                user=request.user,
                following_user=user
            )
            following.delete()
            return Response(
                {"detail": f"You have unfollowed {user.username}."}, 
                status=status.HTTP_200_OK
            )
        except UserFollowing.DoesNotExist:
            return Response(
                {"detail": f"You are not following {user.username}."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def following(self, request):
        following = UserFollowing.objects.filter(user=request.user)
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = UserFollowingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserFollowingSerializer(following, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def followers(self, request):
        followers = UserFollowing.objects.filter(following_user=request.user)
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = UserFollowingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserFollowingSerializer(followers, many=True)
        return Response(serializer.data)


class UserSessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserSession.objects.all()
        return UserSession.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        session = self.get_object()
        if session.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to terminate this session."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        session.is_active = False
        session.save()
        return Response(
            {"detail": "Session terminated successfully."}, 
            status=status.HTTP_200_OK
        )