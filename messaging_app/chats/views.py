from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Conversation 
from .serializers import UserSerializer, ConversationSerializer

# Create a user viewsets
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create a conversation viewsets
class ConversationViewSet(viewsets.ViewSet):
    """
    A viewset for managing the conversation
    """
    def list_conversation(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)