from django.shortcuts import render
# Create your views here.
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invite
from .serializers import InviteSerializer
from rest_framework import viewsets


class InviteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    lookup_field = 'slug'

# class InviteList(APIView):
#     permission_classes = (permissions.AllowAny,)
#     def get(self, request):
#         invites = Invite.objects.all()
#         serializer = InviteSerializer(invites, many=True)
#         return Response(serializer.data)
