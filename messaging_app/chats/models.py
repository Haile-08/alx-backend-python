import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# customize the DRF auth
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Create a user model here.
class User(AbstractBaseUser, PermissionsMixin):
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
    # Use set_password for security
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
                max_length=10,
                choices=Role_Choices,
                null=False,
                default='guest'
            )
    created_at = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

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
