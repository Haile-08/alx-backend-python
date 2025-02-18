import re
from rest_framework import serializers
from .models import User, Message, Conversation


# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    # def validate(self, value):
    #     email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    #     if not re.match(email_regex, value['email']):
    #         raise serializers.ValidationError("Invalid email format.")
    #     return value
    
    def validate_email(self, value):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format.")
        return value


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_number = serializers.CharField(source="sender_id.phone_number")

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'sender_name',
            'conversation_id',
            'message_body',
            'sender_number',
            'sent_at'
            ]

    def get_sender_name(self, obj):
        return f"{obj.sender_id.first_name} {obj.sender_id.last_name}"


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participant_id = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True,)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participant_id',
            'messages',
            'created_at'
            ]

    def get_participant_id(self, obj):
        return [
                f"{participant_id.first_name} {participant_id.last_name}"
                for participant_id in obj.participant_id.all()
            ]
