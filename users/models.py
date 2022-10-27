from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_type_decided=models.BooleanField(default=False) # this is set to true once user type is decided
    image = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    user_type = models.CharField(default='na',max_length=200)
    def __str__(self):
        return f'{self.user.username} Profile'

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    def __str__(self):
        return f'{self.user.username} Patient'

class Hospital(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    def __str__(self):
        return f'{self.user.username} Hospital'