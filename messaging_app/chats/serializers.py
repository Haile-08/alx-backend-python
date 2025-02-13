from rest_framework import serializers
from .models import User, Message, Conversation


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'sender_name', 'conversation', 'message_body', 'sent_at']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, source='messages')
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
