from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ResetUserRegisterForm(forms.Form):
    email_id = forms.EmailField(label='email_id')
    newPassword = forms.CharField(widget=forms.PasswordInput())
    renternewPassword = forms.CharField(widget=forms.PasswordInput())
class UserRegisterForm(forms.Form):
    email_id = forms.EmailField(label='email id')
    password1 = forms.CharField(label='password',widget=forms.PasswordInput())
    password2 = forms.CharField(label='re enter password',widget=forms.PasswordInput())

# test12345
#test 123456
USER_CHOICES = [
    ('Patient','Patient'),
    ('Hospital','Hospital'),
    ('Infirmary','Infirmary'),
    ('InsuranceCompany','InsuranceCompany')
    
]
class UserUpdateForm(forms.ModelForm):
    email_id = forms.EmailField(required=True)

    class Meta:  # configs of the form
        model = User_Auth # form.save() saves it to user model
        fields = ['email_id']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserTypeForm(forms.Form):
    your_type = forms.ChoiceField(choices=USER_CHOICES)
    otp = forms.CharField(label='otp', max_length=10 ,widget= forms.TextInput(attrs={'class':'use-keyboard-input'}))


class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100)
    password  = forms.CharField(label='Password',widget=forms.PasswordInput())
    

class OtpForm(forms.Form):
  otp = forms.CharField(label='otp', max_length=10,widget= forms.TextInput(attrs={'class':'use-keyboard-input'}))


class PatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = ["verification_doc","fullname",'mobile_number']

class HospitalForm(forms.ModelForm):
  class Meta:
    model = Hospital
    fields = ["verification_doc","fullname",'mobile_number',"location",'description','image_1','image_2']

class InfirmaryForm(forms.ModelForm):
  class Meta:
    model = Infirmary
    fields = ["verification_doc","fullname",'mobile_number',"location",'description','image_1','image_2']

class InsuranceCompanyForm(forms.ModelForm):
  class Meta:
    model = InsuranceCompany
    fields = ["verification_doc","fullname",'mobile_number',"location",'description','image_1','image_2']

class PatientForm2(forms.ModelForm):
  class Meta:
    model = Patient
    fields = ["fullname",'mobile_number']

class HospitalForm2(forms.ModelForm):
  class Meta:
    model = Hospital
    fields = ["fullname",'mobile_number',"location",'description','image_1','image_2']

class InfirmaryForm2(forms.ModelForm):
  class Meta:
    model = Infirmary
    fields = ["fullname",'mobile_number',"location",'description','image_1','image_2']

class InsuranceCompanyForm2(forms.ModelForm):
  class Meta:
    model = InsuranceCompany
    fields = ["fullname",'mobile_number',"location",'description','image_1','image_2']

class MedicalDocumentsForm(forms.ModelForm):
    class Meta:
      model = MedicalDocuments
      fields = ['medical_doc','verifier']

class InfirmaryOrderForm(forms.ModelForm):
    class Meta:
      model = InfirmaryOrder
      fields = ['doc','amount_paid','description']

class InsuranceRefundForm(forms.ModelForm):
    class Meta:
      model = InsuranceRefund
      fields = ['doc','refund_amount']


class ViewAccessForm(forms.ModelForm):
    class Meta:
      model = ViewAccess
      fields = ['document','user']


class RequestForm(forms.ModelForm):
    class Meta:
      model = RequestModel
      fields = ['document', 'request']

class DocForm(forms.ModelForm):
    class Meta:
      model = MedicalDocuments
      fields = ['medical_doc']
