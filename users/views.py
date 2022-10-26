from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PatientForm, UserTypeForm
from .models import Patient,Profile
# Create your views here.

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def verify_user(request):
    if request.method == 'POST':     
        v_form=PatientForm(request.POST, instance=request.user.patient)
        if(v_form.is_valid()):
            v_form.save()
            return redirect('profile')
    else:
        p1 = Patient.objects.create(user=request.user,image = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=False)
        v_form=PatientForm(instance=request.user.patient)

    context = {
        'v_form': v_form
    }

    return render(request, 'users/verify.html', context)

@login_required
def get_user_type(request):
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('your_type')
            print("USER TYPE IS ",user_type)
            if(user_type=="Patient"):
                print("YES")
                form2=PatientForm(request.user)
                return redirect('verify')
    else:
        form = UserTypeForm()
    return render(request, 'users/user_type.html', {'form': form})

@login_required
def after_login(request):
    print("after login ",request.user.profile.is_verified)
    if(request.user.profile.is_verified):
        return redirect('profile')
    else:
        return redirect('user_type')