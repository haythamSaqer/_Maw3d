from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

# Create your views here.
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


def get(request):
    user = UserSocialAuth.objects.get_social_auth('google-oauth2', 'harountaha@outlook.sa')
    data = f"Access Token Fro {user} is : {user.extra_data.get('access_token')} ,,, and refresh token is :{user.extra_data.get('refresh_token')}"
    return JsonResponse({'data': data})
