from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Patient,Profile , ViewAccess
from .filters import *
import random
import smtplib
import time
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

@login_required
def verify_user(request):
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

@login_required
def get_user_type(request):
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

@login_required
def after_login(request):
    if(request.user.profile.user_type_decided):
        return redirect('profile')
    else:
        try:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            email = str(request.user.email)
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
    
    if request.method=='POST':
        userpk = request.POST["xyz"]
        request.session['urt'] = userpk
        request.session['drt'] = pk
        print("hey")
        try:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            email = str(request.user.email)
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
    
    


@login_required
def get_hospitals(request):
    hospitals = Hospital.objects.all()
    myFilter = HospitalFilter(request.GET,queryset=hospitals)
    hospitals = myFilter.qs
    return render (request,"users/get_hospitals.html",{'hospitals':hospitals,'myFilter':myFilter})

@login_required
def getDocsH(request):
    docsAll = ViewAccess.objects.filter(user=request.user)
    print(docsAll[0].document.patient.fullname)
    return render (request,"users/getDocsH.html",{'docs':docsAll})

@login_required
def getDocsI(request):
    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/getDocsH.html",{'docs':docsAll})

@login_required
def getDocsP(request):
    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/getDocsH.html",{'docs':docsAll})

@login_required
def get_infirmaries(request):
    if request.method=='POST':
        infirmary_pk = request.POST["infirmary_pk"]
        print(infirmary_pk)
        print("infirmary is: ",Infirmary.objects.get(pk=infirmary_pk))
        return redirect("/place_infirmary_order/"+infirmary_pk)
    infirmaries = Infirmary.objects.all()
    myFilter = InfirmaryFilter(request.GET,queryset=infirmaries)
    infirmaries = myFilter.qs
    return render (request,"users/get_infirmaries.html",{'infirmaries':infirmaries,'myFilter':myFilter})

@login_required
def get_insurancecompanies(request):
    if request.method=='POST':
        insurance_pk = request.POST["insurance_pk"]
        return redirect("/request_insurance_refund/"+insurance_pk)
    insurancecompanies = InsuranceCompany.objects.all()
    myFilter = InsuranceCompanyFilter(request.GET,queryset=insurancecompanies)
    insurancecompanies = myFilter.qs
    return render (request,"users/get_insurancecompanies.html",{'insurancecompanies':insurancecompanies,'myFilter':myFilter})

@login_required
def upload_medical_doc_p(request): 
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

@login_required
def upload_medical_doc_h(request): 
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

@login_required
def place_infirmary_order(request,inf_pk):
    if(request.method=="POST"):
        form = InfirmaryOrderForm(request.POST)
        if(form.is_valid()):
            obj = form.save(commit=False)
            obj.infirmary= Infirmary.objects.get(pk=inf_pk)
            obj.patient = request.user.patient
            obj.save()
            request.user.patient.wallet -= form.cleaned_data.get('amount_paid')
            obj.infirmary.wallet += form.cleaned_data.get('amount_paid')
            # print(request.user.patient.wallet,' ',obj.infirmary.wallet)
            request.user.patient.save()
            obj.infirmary.save()
            return redirect('get_infirmaries')

    form = InfirmaryOrderForm()
    form.fields['doc'].queryset = MedicalDocuments.objects.filter(patient=request.user.patient)
    return render(request, 'users/place_infirmary_order.html', {'form': form})

@login_required
def request_insurance_refund(request,insurance_pk):
    if(request.method=="POST"):
        form = InsuranceRefundForm(request.POST)
        if(form.is_valid()):
            obj = form.save(commit=False)
            obj.insurancecompany= InsuranceCompany.objects.get(pk=insurance_pk)
            obj.patient = request.user.patient
            obj.save()
            return redirect('get_insurancecompanies')

    form = InsuranceRefundForm()
    form.fields['doc'].queryset = MedicalDocuments.objects.filter(patient=request.user.patient)
    return render(request, 'users/request_insurance_refund.html', {'form': form})