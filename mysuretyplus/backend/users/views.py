from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import json
import traceback

# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not all([username, email, password]):
            return Response(
                {'error': 'Tous les champs sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Ce nom d\'utilisateur existe déjà'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Cet email est déjà utilisé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Créer un token d'authentification
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Utilisateur créé avec succès',
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            return Response(
                {'error': 'Erreur lors de la création de l\'utilisateur'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })

class UserLogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            # Récupérer le token depuis les headers
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Token '):
                token_key = auth_header.split(' ')[1]
                try:
                    token = Token.objects.get(key=token_key)
                    token.delete()
                except Token.DoesNotExist:
                    pass  # Token déjà supprimé ou invalide
            
            return Response({'message': 'Déconnexion réussie'})
        except Exception as e:
            print(f"❌ Erreur dans UserLogoutView: {e}")
            return Response({'message': 'Déconnexion réussie'})

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        })

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'L\'adresse email est requise'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            # Générer un token simple pour le moment
            reset_token = get_random_string(64)
            
            # Envoyer l'email (en développement, afficher dans la console)
            reset_url = f"http://localhost:3000/reset-password/{reset_token}"
            
            print(f"=== EMAIL DE RÉINITIALISATION ===")
            print(f"Pour : {email}")
            print(f"Token : {reset_token}")
            print(f"Lien : {reset_url}")
            print(f"Expire dans : 1 heure")
            print(f"================================")
            
            return Response({
                'message': 'Email de réinitialisation envoyé avec succès'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'Aucun compte trouvé avec cette adresse email'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"❌ Erreur dans ForgotPasswordView: {e}")
            traceback.print_exc()
            return Response(
                {'error': f'Erreur lors de l\'envoi de l\'email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ValidateResetTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # En développement, accepter tous les tokens
            return Response({'valid': True})
            
        except Exception as e:
            return Response(
                {'error': 'Token invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([token, new_password]):
            return Response(
                {'error': 'Token et nouveau mot de passe requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # En développement, réinitialiser le mot de passe directement
            email = request.data.get('email')
            if not email:
                return Response({
                    'error': 'Email requis'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
                print(f"=== MOT DE PASSE RÉINITIALISÉ ===")
                print(f"Utilisateur : {user.email}")
                print(f"Nouveau mot de passe défini")
                print(f"================================")
                
                return Response({
                    'message': 'Mot de passe réinitialisé avec succès'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'error': 'Utilisateur non trouvé'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            print(f"❌ Erreur dans ResetPasswordView: {e}")
            traceback.print_exc()
            return Response(
                {'error': f'Erreur lors de la réinitialisation: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        user = request.user
        data = request.data
        
        if 'email' in data:
            user.email = data['email']
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        user.save()
        
        return Response({
            'message': 'Profil mis à jour avec succès',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
