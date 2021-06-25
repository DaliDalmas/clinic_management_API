from django.core.exceptions import ImproperlyConfigured
from django.db import models
from authentication.models import CustomUser
# Create your models here.

class Jwt(models.Model):
    user = models.ForeignKey(CustomUser,related_name="login_user",on_delete=models.CASCADE)
    acess_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    