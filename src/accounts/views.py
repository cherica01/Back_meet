# accounts/views.py
import secrets
import string

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db import IntegrityError
from .models import User, UserFollowing, UserSession, RegistrationRequest
from .permissions import IsOwnerOrReadOnly, IsUserOrAdmin
from .serializers import (UserFollowingSerializer,
                          UserSerializer, UserSessionSerializer,CompleteRegistrationSerializer,
                          InitiateRegistrationSerializer,)
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']
    ordering_fields = ['username', 'date_joined']
    
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
    

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def initiate_registration(request):
    # print("Corps de la requête reçu :", request.data)  # Décode le corps brut en chaîne de caractères
    serializer = InitiateRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = User.objects.normalize_email(serializer.validated_data['email'])
    
    # Vérifier si l'email existe déjà
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email déjà enregistré"}, status=400)
    
    # Générer un code de 6 chiffres
    code = ''.join(secrets.choice(string.digits) for _ in range(6))
    
    # Créer ou mettre à jour la demande d'inscription
    RegistrationRequest.objects.update_or_create(
        email=email,
        defaults={'code': code, 'created_at': timezone.now()}
    )
    
    # Envoyer le code par email (à remplacer par une tâche asynchrone en production)
    send_mail(
        'Votre code de vérification HackITech',
        f'Votre code de vérification est : {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    
    return Response({"message": "Code de vérification envoyé par email"})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def complete_registration(request):
    serializer = CompleteRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    email = User.objects.normalize_email(serializer.validated_data['email'])
    code = serializer.validated_data['code']
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    # Récupérer la demande d'inscription
    try:
        registration_request = RegistrationRequest.objects.filter(email=email).latest('created_at')
    except RegistrationRequest.DoesNotExist:
        print("Aucune demande d'inscription trouvée pour l'email:", email)
        return Response({"error": "Aucune demande d'inscription trouvée"}, status=400)
    
    # Vérifier le code et l'expiration
    if registration_request.code != code:
        print("Code invalide pour l'email:", email)
        return Response({"error": "Code invalide"}, status=400)
    
    if registration_request.is_expired():
        
        print("Code expiré pour l'email:", email)
        return Response({"error": "Code expiré"}, status=400)
    
    # Vérifier le nom d'utilisateur
    if User.objects.filter(username=username).exists():
        print("Nom d'utilisateur déjà pris:", username)
        return Response({"error": "Nom d'utilisateur déjà pris"}, status=505)
    
    # Créer l'utilisateur
    try:
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            is_verified=True
        )
    except IntegrityError:
        return Response({"error": "Erreur lors de la création du compte"}, status=400)
    
    # Supprimer la demande d'inscription
    registration_request.delete()
    
    return Response({
        "message": "Compte créé avec succès",
        "user_id": user.id,
        "email": user.email,
        "username": user.username
    })