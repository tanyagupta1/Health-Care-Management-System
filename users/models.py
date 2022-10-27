from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified=models.BooleanField(default=False) # this is set to true once user type is decided
    image = models.FileField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(default='default.jpg',upload_to='profile_pics')
    fullname = models.CharField(max_length=200)
    mobile_number = models.IntegerField() 
    is_verified = models.BooleanField(default=False) # set true after document verification
    def __str__(self):
        return f'{self.user.username} Profile'
