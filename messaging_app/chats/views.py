from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# Create a user viewsets
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create a conversation viewsets
class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'participant_id__first_name',
        'participant_id__last_name',
        'participant_id__email'
        ]

    def create(self, request):
        """
        Override the modal view set create method to create
        conversation with one or more participants.
        Request:
            {
                "participants_id": [
                    "076b2a46-376c-4656-90c5-07cb186ce690",
                    "ea561865-dc57-44c1-bcb1-6d2dd36debd9"
                    ]
            }
        """
        participants_id = request.data.get('participants_id', [])

        # check if there is participants ids specified has two participants
        if not participants_id or len(participants_id) < 2: 
            return Response(
                {'Error:': 'At least two participants in the conversation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure all the participants exist in the user modal
        # check all the participants id are in user
        # input [1,2,3] check using user_id__in checks array of ids
        # QuerySet Field Lookups Reference
        participants = User.objects.filter(user_id__in=participants_id)
        if len(participants) != len(participants_id):
            return Response(
                {'Error:': 'One or more users do not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new conversation
        conversation = Conversation.objects.create()
        conversation.participant_id.set(participants)
        conversation.save()
        serialized_conversation = ConversationSerializer(conversation).data

        return Response(
            serialized_conversation,
            status=status.HTTP_200_OK
        )


# Create a message viewsets
class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the message
    Request:
        {
            "sender_id": "076b2a46376c465690c507cb186ce690",
            "conversation_id": "694cff0b-eeee-4ceb-bdb2-a371a374b866",
            "message_body": "Hello world"
        }
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sender_id__first_name', 'sender_id__last_name', 'message_body']

    def create(self, request):
        """
        Override the modal view set create method to send
        a message to one or more participants.
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        # check if the conversation id is specified
        if not conversation_id:
            return Response(
                {'Error:': 'conversation_id not specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check if the sender id is specified
        if not sender_id:
            return Response(
                {'Error:': 'sender not specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check if the message body is specified
        if not message_body:
            return Response(
                {'Error:': 'message not specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check if the conversation id exist in the database
        conversation_exist = Conversation.objects.get(conversation_id=conversation_id)
        if not conversation_exist:
            return Response(
                {'Error:': 'conversation not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # check if the sender is in the conversation
        if sender_id not in conversation_exist.participant_id.all():
            return Response(
                {'Error:': 'You are not part of this conversation..'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            message_body=message_body,
        )

        serialized_message = MessageSerializer(message).data
        return Response(
            serialized_message,
            status=status.HTTP_200_OK
        )