import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create a user model here.
class User(models.Model):
    class Role_Choices(models.TextChoices):
        GUEST = "guest", _("guest")
        HOST = "host", _("host")
        ADMIN = "admin", _("admin")

    user_id = models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                editable=False
            )
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(null=False, unique=True)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
                max_length=10,
                choices=Role_Choices,
                null=False,
                default='guest'
            )
    created_at = models.DateField(auto_now_add=True)

    def get_full_name(self):
        return f"NAME: {self.first_name} {self.last_name}"

    def __str__(self):
        return f"USER: {self.first_name} {self.last_name}: ({self.email})"


# Create a conversation model here.
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    participant_id = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


# Create a message model here.
class Message(models.Model):
    message_id = models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                db_index=True
            )
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(
                    Conversation,
                    on_delete=models.CASCADE,
                    related_name="messages"
                )
    message_body = models.TextField(null=False)
    sent_at = models.DateField(auto_now_add=True)
