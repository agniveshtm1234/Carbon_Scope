from django.db import models

# Create your models here. 
from django.contrib.auth.models import User
import uuid

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
