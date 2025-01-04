from django.contrib.auth.models import AbstractUser
from django.db import models 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birthdate = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, related_name='preferences', on_delete=models.CASCADE)
    currency = models.CharField(max_length=20, default="USD")
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Prefereces"