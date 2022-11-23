from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Patient,Profile , ViewAccess , User_Auth
from .filters import *
import random
import smtplib
import time
import hashlib
# Create your views here.

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            passwordHash = hashlib.sha256(password.encode()).hexdigest()
            email_id = form.cleaned_data.get('email')
            h1 = User_Auth.objects.create(
                email_id = form.cleaned_data.get('email'),
                password_hash = passwordHash)
            print(h1)
            Profile.objects.create(user = h1)
            messages.success(request,f'Account created for {email_id}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


def login(request):

    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            passwordHash = hashlib.sha256(password.encode()).hexdigest()
            passReterive  =User_Auth.objects.filter(email_id = email)[0].password_hash
            if ( passwordHash==passReterive):
                #user ko set krna hai 
                request.user = User_Auth.objects.filter(email_id = email)[0]
                print (request.user)
                request.session['user'] = email
                return redirect('after_login')
            else:
                messages.error(request, "Sahi password daal re bc  ")
                return redirect("login")
            
    else:
        form = LoginForm()
    return render(request,'users/login.html',{'form':form})        



def profile(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        user_type_form=''
        if(request.user.profile.user_type=="Patient"):
            user_type_form = PatientForm(request.POST,request.FILES,instance = request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):
            user_type_form = HospitalForm(request.POST,request.FILES,instance = request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):
            user_type_form = InfirmaryForm(request.POST,request.FILES,instance = request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):
            user_type_form = InsuranceCompanyForm(request.POST,request.FILES,instance = request.user.insurancecompany)
        if u_form.is_valid() and p_form.is_valid() and user_type_form.is_valid():
            u_form.save()
            p_form.save()
            user_type_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        user_type_form=''
        if(request.user.profile.user_type=="Patient"):
            user_type_form =PatientForm(instance = request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):
            user_type_form =HospitalForm(instance = request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):
            user_type_form =InfirmaryForm(instance = request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):
            user_type_form =InsuranceCompanyForm(instance = request.user.insurancecompany)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_type_form':user_type_form
    }

    return render(request, 'users/profile.html', context)


def verify_user(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method == 'POST':  
        if(request.user.profile.user_type=="Patient"):   
            v_form=PatientForm(request.POST, instance=request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):   
            v_form=HospitalForm(request.POST, instance=request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):   
            v_form=InfirmaryForm(request.POST, instance=request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):   
            v_form=InsuranceCompanyForm(request.POST, instance=request.user.insurancecompany)
        if(v_form.is_valid()):
            v_form.save()
            return redirect('profile')
    else:
        if(request.user.profile.user_type=="Patient"):   
            v_form=PatientForm(instance=request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):   
            v_form=HospitalForm(instance=request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):   
            v_form=InfirmaryForm(instance=request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):   
            v_form=InsuranceCompanyForm(instance=request.user.insurancecompany)

    context = {
        'v_form': v_form
    }
    return render(request, 'users/verify.html', context)


def get_user_type(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('your_type')
            otp = request.session.get('otp')
            if (str(otp) == str(form.cleaned_data.get('otp'))):
                print("hahahah")
            else:
                return redirect("login")
            print("USER TYPE IS ",user_type)
            request.user.profile.user_type_decided=True
            request.user.profile.user_type = user_type
            request.user.profile.save()
            if(user_type=="Patient"):
                p1 = Patient.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=False)
            elif(user_type=="Hospital"):
                h1 = Hospital.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=False)
            elif(user_type=="Infirmary"):
                i1 = Infirmary.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=False)
            elif(user_type=="InsuranceCompany"):
                ic1 = InsuranceCompany.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=False)
            
            return redirect('verify')
    else:
        form = UserTypeForm()
    return render(request, 'users/user_type.html', {'form': form})


def after_login(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    
    try:
        if(request.user.profile.user_type_decided):
            return redirect('profile')
    except:
        print("ff")
        pass
    if ( 1==2):
        return redirect("login")
    else:
        try:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            email = str(request.user.email_id)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("agarg19030@gmail.com", "kgsbxtxqjjtoddwk")
            s.sendmail("msg", email,"your otp is"+ str(otp))
            print("Success")
        except Exception as e:
            print(e)
            return redirect('login')
                # messages.error(request,"Sorry. some trouble")
        return redirect('user_type')         # return redirect('register')

def doc_share_otp(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            userkey = request.session.get('urt')
            otp = request.session.get('otp')
            if (str(otp) == str(form.cleaned_data.get('otp'))):
                print("hahahah")
                dockey = request.session.get('drt')
                medDoc = MedicalDocuments.objects.filter(pk=dockey)[0]
                user2 = User.objects.filter(pk =userkey)[0]
                h1 = ViewAccess.objects.create(document = medDoc,  user=user2)
                return redirect('upload_medical_doc_p')
                

    form = OtpForm()
    return render(request,"users/doc_share_otp.html" , {"form": form})

def ShareDocP(request , pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        userpk = request.POST["xyz"]
        request.session['urt'] = userpk
        request.session['drt'] = pk
        print("hey")
        try:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            email = str(request.user.email_id)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("agarg19030@gmail.com", "kgsbxtxqjjtoddwk")
            s.sendmail("msg", email,"your otp is"+ str(otp))
            print("Success")
            return redirect("doc_share_otp")
        except:
            pass
    
    hospitalsAll = Hospital.objects.all()
    infirmariesAll = Infirmary.objects.all()
    insurancecompaniesAll = InsuranceCompany.objects.all()
    
    return render(request,"users/ShareDocP.html" , {
        "hospitalsAll" : hospitalsAll ,
        "infirmariesAll" :infirmariesAll , 
        "insurancecompaniesAll" : insurancecompaniesAll, 
    })


def get_hospitals(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    hospitals = Hospital.objects.all()
    myFilter = HospitalFilter(request.GET,queryset=hospitals)
    hospitals = myFilter.qs
    return render (request,"users/get_hospitals.html",{'hospitals':hospitals,'myFilter':myFilter})


def getDocsH(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/getDocsH.html",{'docs':docsAll})


def getDocsI(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/getDocsH.html",{'docs':docsAll})


def getDocsP(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/getDocsH.html",{'docs':docsAll})


def get_infirmaries(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    infirmaries = Infirmary.objects.all()
    myFilter = InfirmaryFilter(request.GET,queryset=infirmaries)
    infirmaries = myFilter.qs
    return render (request,"users/get_infirmaries.html",{'infirmaries':infirmaries,'myFilter':myFilter})


def get_insurancecompanies(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    insurancecompanies = InsuranceCompany.objects.all()
    myFilter = InsuranceCompanyFilter(request.GET,queryset=insurancecompanies)
    insurancecompanies = myFilter.qs
    return render (request,"users/get_insurancecompanies.html",{'insurancecompanies':insurancecompanies,'myFilter':myFilter})


def upload_medical_doc_p(request): 
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    print("hello")
    if request.method=='POST':
        print(request.POST)
        form = MedicalDocumentsFormPatient(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.patient= request.user.patient
            obj.save()
            return redirect('upload_medical_doc_p')
    else:
        form = MedicalDocumentsFormPatient()
    docs = MedicalDocuments.objects.filter(patient=request.user.patient)
    print(docs)
    return render(request, 'users/upload_medical_doc.html', {'form': form,'docs':docs})



    


def upload_medical_doc_h(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        form = MedicalDocumentsFormHospital(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.hospital= request.user.hospital
            obj.is_verified = True
            obj.save()
            return redirect('upload_medical_doc_h')
    else:
        form = MedicalDocumentsFormHospital()
    docs = MedicalDocuments.objects.filter(hospital=request.user.hospital)
    return render(request, 'users/upload_medical_doc.html', {'form': form,'docs':docs})



