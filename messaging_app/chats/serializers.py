from rest_framework import serializers
from .models import User, Message, Conversation


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'sender_name',
            'conversation',
            'message_body',
            'sent_at'
            ]

    def get_sender_name(self, obj):
        return f"{obj.sender_id.first_name} {obj.sender_id.last_name}"


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True,)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participant_id',
            'messages',
            'created_at'
            ]

    def get_participants(self, obj):
        return [
                f"{participant.first_name} {participant.last_name}"
                for participant in obj.participant_id.all()
            ]
