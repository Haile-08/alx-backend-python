from rest_framework.permissions import BasePermission

class IsInTheConversation(BasePermission):
    """
    Custom permission to allow only users (participants) who are in the convo to view a conversation.
    https://testdriven.io/blog/custom-permission-classes-drf/
    """

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is a participant in the conversation
        # where the obj is in the conversation modal
        return request.user in obj.participant_id.all()


class IsSenderOfMessage(BasePermission):
    """
    Custom permission to allow only the sender to view or modify a message.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the sender of the message
        # where the obj is in the message modal
        return request.user == obj.sender_id