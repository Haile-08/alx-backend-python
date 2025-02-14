from django.shortcuts import render
from rest_framework import status
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
    def list(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
