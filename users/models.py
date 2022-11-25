from django.db import models
from django.contrib.auth.models import User
# Create your models here
# 
# 
# .



class User_Auth(models.Model):
    email_id = models.CharField(default='na', max_length = 200 , primary_key=True)
    password_hash = models.CharField(default='na', max_length = 512)
    is_authenticated = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email_id} User_Password'

class Profile(models.Model):
    user = models.OneToOneField(User_Auth ,on_delete=models.CASCADE)
    user_type_decided=models.BooleanField(default=False) # this is set to true once user type is decided
    image = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    user_type = models.CharField(default='na',max_length=200)
    def __str__(self):
        return f'{self.user.email_id} Profile'

class Patient(models.Model):
    user = models.OneToOneField(User_Auth,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    wallet = models.IntegerField(default=1000000,null=True)
    def __str__(self):
        return f'{self.user.email_id} Patient'

class Hospital(models.Model):
    user = models.OneToOneField(User_Auth,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    location = models.CharField(default="Delhi",max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    description = models.TextField(default="na",null=True)
    image_1 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    image_2 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    def __str__(self):
        return f'{self.user.email_id} Hospital'

class Infirmary(models.Model):
    user = models.OneToOneField(User_Auth,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    location = models.CharField(default="Delhi",max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    wallet = models.IntegerField(default=1000000,null=True)
    description = models.TextField(default="na",null=True)
    image_1 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    image_2 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    def __str__(self):
        return f'{self.user.email_id} Infirmary'

class InsuranceCompany(models.Model):
    user = models.OneToOneField(User_Auth,on_delete=models.CASCADE)
    verification_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    fullname = models.CharField(max_length=200,null=True)
    location = models.CharField(default="Delhi",max_length=200,null=True)
    mobile_number = models.IntegerField(null=True) 
    is_verified = models.BooleanField(default=False,null=True) # set true after document verification
    description = models.TextField(default="na",null=True)
    image_1 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    image_2 = models.ImageField(default='default.jpg',upload_to='profile_pics',null=True)
    wallet = models.IntegerField(default=1000000,null=True)
    def __str__(self):
        return f'{self.user.email_id} InsuranceCompany'




class MedicalDocuments(models.Model):
    owner = models.ForeignKey(User_Auth,on_delete=models.CASCADE,null=True)
    medical_doc= models.FileField(default='default.jpg',upload_to='profile_pics',null=True)
    is_verified = models.BooleanField(default=False,null=True) 
    def __str__(self):
        return f'{self.owner.email_id} Medical Doc'


class ViewAccess(models.Model):
    document = models.ForeignKey(MedicalDocuments,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User_Auth,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return "Access"

class InfirmaryOrder(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    infirmary = models.ForeignKey(Infirmary,on_delete=models.CASCADE,null=True)
    doc = models.ForeignKey(MedicalDocuments,on_delete=models.CASCADE,null=True)
    amount_paid = models.IntegerField(default=0,null=True)
    description = models.TextField(default="na",null=True)
    def __str__(self):
        return f'{self.patient.fullname} {self.infirmary.fullname} Infirmary Order'

class InsuranceRefund(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    insurance_company = models.ForeignKey(InsuranceCompany,on_delete=models.CASCADE,null=True)
    doc = models.ForeignKey(MedicalDocuments,on_delete=models.CASCADE,null=True)
    refund_amount= models.IntegerField(default=0,null=True)
    def __str__(self):
        return f'Insurance Refund'

class DocRequestHospital(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True)
    is_fulfilled = models.BooleanField(default=False,null=True)
    def __str__(self):
        return f'DocRequestHospital'