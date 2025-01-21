import uuid
from django.db import models


# Create a user model here.
class User(models.Model):
    ROLE_CHOICES = {
        'guest': 'guest',
        'host': 'host',
        'admin': 'admin',
    }

    user_id = models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                db_index=True
            )
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(null=False, unique=True)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(null=True, blank=True)
    role = models.CharField(
                max_length=10,
                choices=ROLE_CHOICES,
                null=False,
                default='guest'
            )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"- {self.first_name} {self.last_name}: ({self.email})"


