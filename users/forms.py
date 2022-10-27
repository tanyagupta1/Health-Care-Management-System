from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Patient
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:  # configs of the form
        model = User # form.save() saves it to user model
        fields = ['username','email','password1','password2']

# test12345
#test 123456

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:  # configs of the form
        model = User # form.save() saves it to user model
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserTypeForm(forms.Form):
    your_type = forms.CharField(label='Patient/Doctor/Insurance', max_length=100)

class PatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = ["image","fullname",'mobile_number']

class UserTypeSpecificUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['image','fullname','mobile_number']