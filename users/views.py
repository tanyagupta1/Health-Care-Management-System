from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Patient,Profile , ViewAccess , User_Auth
from .filters import *
from django.http.response import FileResponse
from django.http import HttpResponseForbidden
import random
import smtplib
import time
import hashlib
import base64
# Create your views here.

def add_money(request): 
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        amount  = int(request.POST.get("amount"))
        if(amount<0):
            return HttpResponseForbidden("negative money not allowed")
        if(request.user.profile.user_type=="Patient"):
            request.user.patient.wallet += amount
            request.user.patient.save()   
        if(request.user.profile.user_type=="Infirmary"):
            request.user.infirmary.wallet += amount
            request.user.infirmary.save()
        if(request.user.profile.user_type=="InsuranceCompany"):
            request.user.insurancecompany.wallet += amount
            request.user.insurancecompany.save()

    return render(request,'users/add_money.html')

def media_access(request, file): 
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    print("HERE")
    try:
        doc=MedicalDocuments.objects.filter(medical_doc="profile_pics/"+file).first()
        view_access = ViewAccess.objects.filter(user = request.user,document = doc).first()
        print(doc,"HI",view_access)
        if(view_access ==None ):
            doc=None
            #check profile pic and verification doc
            if(request.user.profile.user_type=="Patient"):
                doc=Profile.objects.filter(image="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.image)
                doc=Patient.objects.filter(verification_doc="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.verification_doc)
            elif(request.user.profile.user_type=="Hospital"):
                doc=Profile.objects.filter(image="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.image)
                doc=Hospital.objects.filter(verification_doc="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.verification_doc)
            elif(request.user.profile.user_type=="Infirmary"):
                doc=Profile.objects.filter(image="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.image)
                doc=Infirmary.objects.filter(verification_doc="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.verification_doc)
            elif(request.user.profile.user_type=="InsuranceCompany"):
                doc=Profile.objects.filter(image="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.image)
                doc=InsuranceCompany.objects.filter(verification_doc="profile_pics/"+file,user=request.user).first()
                if(doc!=None):
                    return FileResponse(doc.verification_doc)
            return HttpResponseForbidden("Forbidden")
        else:
            return FileResponse(doc.medical_doc)
    except :
        
        return HttpResponseForbidden("Forbidden")
#     path,file_name=os.path.split(file)
#     response=FileResponse(document.medical_doc)
#     return response

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            passwordHash = hashlib.sha256(password.encode()).hexdigest()
            email_id = form.cleaned_data.get('email_id')
            h1 = User_Auth.objects.create(
                email_id = form.cleaned_data.get('email_id'),
                password_hash = passwordHash)
            print(h1)
            Profile.objects.create(user = h1)
            messages.success(request,f'Account created for {email_id}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    # return render(request , "users/sign.html")
    return render(request,'users/register.html',{'form':form})


def login(request):

    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
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
            except:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
            
    else:
        
        form = LoginForm()
    return render(request,'users/login.html',{'form':form})        



def profile(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        user_type_form=''
        if(request.user.profile.user_type=="Patient"):
            if(request.user.patient.is_verified):
                user_type_form = PatientForm2(request.POST,request.FILES,instance = request.user.patient)
            else:
                user_type_form = PatientForm(request.POST,request.FILES,instance = request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):
            if(request.user.hospital.is_verified):
                print("HEEEEEEREEEEE")
                user_type_form = HospitalForm2(request.POST,request.FILES,instance = request.user.hospital)
            else:
                user_type_form = HospitalForm(request.POST,request.FILES,instance = request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):
            if(request.user.infirmary.is_verified):
                user_type_form = InfirmaryForm2(request.POST,request.FILES,instance = request.user.infirmary)
            else:
                user_type_form = InfirmaryForm(request.POST,request.FILES,instance = request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):
            if(request.user.insurancecompany.is_verified):
                user_type_form = InsuranceCompanyForm2(request.POST,request.FILES,instance = request.user.insurancecompany)
            else:
                user_type_form = InsuranceCompanyForm(request.POST,request.FILES,instance = request.user.insurancecompany)
        if p_form.is_valid() and user_type_form.is_valid():
            p_form.save()
            user_type_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        user_type_form=''
        if(request.user.profile.user_type=="Patient"):
            if(request.user.patient.is_verified):
                user_type_form = PatientForm2(instance = request.user.patient)
            else:
                user_type_form = PatientForm(instance = request.user.patient)
        elif(request.user.profile.user_type=="Hospital"):
            if(request.user.hospital.is_verified):
                print("HEEEEEEREEEEE")
                user_type_form = HospitalForm2(instance = request.user.hospital)
            else:
                user_type_form = HospitalForm(instance = request.user.hospital)
        elif(request.user.profile.user_type=="Infirmary"):
            if(request.user.infirmary.is_verified):
                user_type_form = InfirmaryForm2(instance = request.user.infirmary)
            else:
                user_type_form = InfirmaryForm(instance = request.user.infirmary)
        elif(request.user.profile.user_type=="InsuranceCompany"):
            if(request.user.insurancecompany.is_verified):
                user_type_form = InsuranceCompanyForm2(instance = request.user.insurancecompany)
            else:
                user_type_form = InsuranceCompanyForm(instance = request.user.insurancecompany)
        if p_form.is_valid() and user_type_form.is_valid():
            p_form.save()
            user_type_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        context = {'p_form': p_form,'user_type_form':user_type_form}
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
                p1 = Patient.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=True)
            elif(user_type=="Hospital"):
                h1 = Hospital.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=True)
            elif(user_type=="Infirmary"):
                i1 = Infirmary.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=True)
            elif(user_type=="InsuranceCompany"):
                ic1 = InsuranceCompany.objects.create(user=request.user,verification_doc = 'default.jpg',fullname='na',mobile_number = 12345,is_verified=True)
            
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
            # s = smtplib.SMTP('smtp.gmail.com', 587)
            # s.starttls()
            # s.login("agarg19030@gmail.com", "kgsbxtxqjjtoddwk")
            # s.sendmail("msg", email,"your otp is"+ str(otp))
            # print("Success")
            print("OTP is ",str(otp))
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
                print("OTP matched")
                dockey = request.session.get('drt')
                medDoc = MedicalDocuments.objects.filter(pk=dockey)[0]
                print("USER KEY is ",str(userkey))
                user2 = User_Auth.objects.filter(pk =userkey)[0]
                h1 = ViewAccess.objects.create(document = medDoc,  user=user2)
                return redirect('share_docs')
                

    form = OtpForm()
    return render(request,"users/doc_share_otp.html" , {"form": form})

def ShareDocP(request , pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        userpk = request.POST["xyz"]
        request.session['urt'] = userpk
        print(userpk)
        request.session['drt'] = pk
        print("hey")
        try:
            otp=random.randint(1000,9999)
            request.session['otp'] = otp
            # email = str(request.user.email_id)
            # s = smtplib.SMTP('smtp.gmail.com', 587)
            # s.starttls()
            # s.login("agarg19030@gmail.com", "kgsbxtxqjjtoddwk")
            # s.sendmail("msg", email,"your otp is"+ str(otp))
            print("Share OTP is ",otp)
            print("Success")
            return redirect("doc_share_otp")
        except:
            pass
    
    hospitalsAll = Hospital.objects.all()
    infirmariesAll = Infirmary.objects.all()
    insurancecompaniesAll = InsuranceCompany.objects.all()
    patientsAll = Patient.objects.all()

    return render(request,"users/ShareDocP.html" , {
        "hospitalsAll" : hospitalsAll ,
        "infirmariesAll" :infirmariesAll , 
        "insurancecompaniesAll" : insurancecompaniesAll, 
        "patientsAll" : patientsAll, 
    })


def get_hospitals(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        hospital_pk = request.POST["hospital_pk"]
        print(hospital_pk)
        print("hospital is: ",Hospital.objects.get(pk=hospital_pk))
        DocRequestHospital.objects.create(patient=request.user.patient,hospital =Hospital.objects.get(pk=hospital_pk) )
    hospitals = Hospital.objects.all()
    myFilter = HospitalFilter(request.GET,queryset=hospitals)
    hospitals = myFilter.qs

    allrequests = DocRequestHospital.objects.filter(patient=request.user.patient)
    print(allrequests)
    return render (request,"users/get_hospitals.html",{'hospitals':hospitals,'myFilter':myFilter , "allreq" : allrequests})

@csrf_exempt
def sign(request):
    if request.method=='POST':
        id_data  = request.POST["idData"];
        hashVal = request.POST["data"];
        mydoc = MedicalDocuments.objects.filter(pk = id_data)[0]
        mydoc.is_verified = True
        mydoc.save()
        return redirect("check")
    
    h1 = request.session['hash']
    docid = request.session['ids']
    return render(request , "users/sign.html" , {"hash" : h1 , "doc" : docid} )
    



def verifydoc(request): 
    ids = request.session["docccccd"]
    mydoc = MedicalDocuments.objects.filter(pk = ids)[0]
    docurl = str(mydoc.medical_doc.url)[1:]
    # print(docurl)
    # print(docurl)
    h1 = ""
    with open(docurl , "rb") as f:
        encoded_string = base64.b64encode(f.read())
        h1 =  hashlib.sha256(encoded_string).hexdigest()
    print(h1)
    return render(request , "users/verifydoc.html" , {"hash" : h1 , "doc" : ids }); 

def get_shared_docs(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]

    if request.method=='POST' and 'view_doc' in request.POST:
        ids = request.POST["dis"]
        request.session["docccccd"] = ids

        return redirect("verifydoc")
        
    if request.method=='POST':
        ids = request.POST["xyz"]
        mydoc = MedicalDocuments.objects.filter(pk = ids)[0]
        docurl = str(mydoc.medical_doc.url)[1:]
        h1 = ""
        with open(docurl , "rb") as f:
            encoded_string = base64.b64encode(f.read())
            h1 =  hashlib.sha256(encoded_string).hexdigest()
        
        request.session['hash'] = h1
        request.session['ids'] = ids
        return redirect("sign")

    docsAll = ViewAccess.objects.filter(user=request.user)
    return render (request,"users/get_shared_docs.html",{'docs':docsAll })




   
    

def check(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    return render(request, "users/check.html");
def get_infirmaries(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        infirmary_pk = request.POST["infirmary_pk"]
        print(infirmary_pk)
        print("infirmary is: ",Infirmary.objects.get(pk=infirmary_pk))
        return redirect("/place_infirmary_order/"+infirmary_pk)
    infirmaries = Infirmary.objects.all()
    myFilter = InfirmaryFilter(request.GET,queryset=infirmaries)
    infirmaries = myFilter.qs
    return render (request,"users/get_infirmaries.html",{'infirmaries':infirmaries,'myFilter':myFilter})


def get_insurancecompanies(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST':
        insurance_pk = request.POST["insurance_pk"]
        return redirect("/request_insurance_refund/"+insurance_pk)
    insurancecompanies = InsuranceCompany.objects.all()
    myFilter = InsuranceCompanyFilter(request.GET,queryset=insurancecompanies)
    insurancecompanies = myFilter.qs
    return render (request,"users/get_insurancecompanies.html",{'insurancecompanies':insurancecompanies,'myFilter':myFilter})

def upload_medical_doc(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST' and 'upload_doc' in request.POST:
        form = MedicalDocumentsForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner= request.user
            if(request.user.profile.user_type=='Hospital'):
                obj.is_verified = False
            obj.save()
            ViewAccess.objects.create(document = obj,user=obj.owner)
            if(request.user.profile.user_type=='Patient'):
                ViewAccess.objects.create(document = obj,user=obj.verifier.user)
            return redirect('upload_medical_doc')
    elif request.method=='POST' and 'share' in request.POST:
        form = ViewAccessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_medical_doc')
    else:
        form = MedicalDocumentsForm()
    docs = MedicalDocuments.objects.filter(owner=request.user)
    if(request.user.profile.user_type=='Hospital'):
        form.fields['verifier'].queryset = Hospital.objects.filter(pk=request.user.hospital.pk)
    return render(request, 'users/upload_medical_doc.html', {'form': form,'docs':docs })

def share_docs(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]   
    if request.method=='POST' and 'share' in request.POST:
        form = ViewAccessForm(request.POST)
        if form.is_valid():
            # form.save()
            # return redirect('share_docs')
            print(form.cleaned_data)
            request.session['urt'] = form.cleaned_data.get('user').pk
            request.session['drt'] = form.cleaned_data.get('document').pk
            try:
                otp=random.randint(1000,9999)
                request.session['otp'] = otp
                # email = str(request.user.email_id)
                # s = smtplib.SMTP('smtp.gmail.com', 587)
                # s.starttls()
                # s.login("agarg19030@gmail.com", "kgsbxtxqjjtoddwk")
                # s.sendmail("msg", email,"your otp is"+ str(otp))
                print("Share OTP is ",otp)
                print("Success")
                return redirect("doc_share_otp")
            except:
                pass

    else:
        form = ViewAccessForm()
        l1 = list(ViewAccess.objects.filter(user__pk=request.user.pk).values_list('document',flat=True))
        form.fields['document'].queryset = MedicalDocuments.objects.filter(pk__in = l1,is_verified=True)
        form.fields['user'].queryset = (User_Auth.objects.exclude(profile__user_type='Patient')).filter(profile__user_type_decided=True)
        if(request.user.profile.user_type=='Hospital'):
            form.fields['user'].queryset = User_Auth.objects.filter(profile__user_type='Patient')
            form.fields['document'].queryset = MedicalDocuments.objects.filter(owner=request.user,is_verified=True)
    return render(request, 'users/share_docs.html', {'form': form })

# #@loggin_required
def place_infirmary_order(request,inf_pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if(request.method=="POST"):
        form = InfirmaryOrderForm(request.POST)
        if(form.is_valid()):
            amount=form.cleaned_data.get('amount_paid')
            if(amount<0):
                return HttpResponseForbidden("negative money not allowed")
            obj = form.save(commit=False)
            obj.infirmary= Infirmary.objects.get(pk=inf_pk)
            obj.patient = request.user.patient
            obj.save()
            # request.user.patient.wallet -= form.cleaned_data.get('amount_paid')
            # obj.infirmary.wallet += form.cleaned_data.get('amount_paid')
            # # print(request.user.patient.wallet,' ',obj.infirmary.wallet)
            # request.user.patient.save()
            # obj.infirmary.save()
            # file_loc = 'media/profile_pics/'+str(obj.pk)+'.txt'
            # f = open(file_loc, 'w')
            # f.writelines(str(form.cleaned_data.get('amount_paid')))
            # f.writelines('\n')
            # f.writelines(obj.description)
            # f.close()
            # doc_loc = 'profile_pics/'+str(obj.pk)+'.txt'
            # new_doc = MedicalDocuments.objects.create(owner=obj.infirmary.user,medical_doc=doc_loc,is_verified=True,verifier=None)
            # ViewAccess.objects.create(document = new_doc,user=request.user)
            # ViewAccess.objects.create(document = new_doc,user=obj.infirmary.user)
            return redirect('get_infirmaries')
        else:
            print(form.errors.as_data())
    infirmary_auth_pk = Infirmary.objects.get(pk=inf_pk).user.pk
    form = InfirmaryOrderForm()
    patient_access = list(ViewAccess.objects.filter(user__pk=request.user.pk).values_list('document',flat=True))
    infirmary_access = list(ViewAccess.objects.filter(user__pk=infirmary_auth_pk).values_list('document',flat=True))
    l1 = set(patient_access).intersection(infirmary_access)
    form.fields['doc'].queryset = MedicalDocuments.objects.filter(pk__in = l1)
    
    return render(request, 'users/place_infirmary_order.html', {'form': form})

# @login_required
def request_insurance_refund(request,insurance_pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if(request.method=="POST"):
        form = InsuranceRefundForm(request.POST)
        if(form.is_valid()):
            obj = form.save(commit=False)
            obj.insurance_company= InsuranceCompany.objects.get(pk=insurance_pk)
            obj.patient = request.user.patient
            obj.save()
            return redirect('get_insurancecompanies')

    
    insurance_auth_pk = InsuranceCompany.objects.get(pk=insurance_pk).user.pk
    form = InsuranceRefundForm()
    patient_access = list(ViewAccess.objects.filter(user__pk=request.user.pk).values_list('document',flat=True))
    insurance_access = list(ViewAccess.objects.filter(user__pk=insurance_auth_pk).values_list('document',flat=True))
    print(patient_access)
    print(insurance_access)
    l1 = set(patient_access).intersection(insurance_access)
    form.fields['doc'].queryset = MedicalDocuments.objects.filter(pk__in = l1)

    return render(request, 'users/request_insurance_refund.html', {'form': form})

#@loggin_required
def get_insurance_refund_requests(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    refund_requests = InsuranceRefund.objects.filter(insurance_company = request.user.insurancecompany)
    return render (request,"users/get_insurance_refund_requests.html",{'requests':refund_requests})

#@loggin_required
def get_infirmary_orders(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if(request.method=="POST"):
        request_pk = request.POST["request_pk"]
        obj = InfirmaryOrder.objects.get(pk=request_pk)
        
        obj.patient.wallet -= obj.amount_paid
        obj.infirmary.wallet += obj.amount_paid
        obj.patient.save()
        obj.infirmary.save()
        Transactions.objects.create(sender = obj.patient.user,receiver=obj.infirmary.user,amount=obj.amount_paid)
        file_loc = 'media/profile_pics/'+str(obj.pk)+'.txt'
        f = open(file_loc, 'w')
        f.writelines(str(obj.amount_paid))
        f.writelines('\n')
        f.writelines(obj.description)
        f.close()
        doc_loc = 'profile_pics/'+str(obj.pk)+'.txt'
        new_doc = MedicalDocuments.objects.create(owner=obj.infirmary.user,medical_doc=doc_loc,is_verified=True,verifier=None)
        ViewAccess.objects.create(document = new_doc,user=obj.patient.user)
        ViewAccess.objects.create(document = new_doc,user=obj.infirmary.user)
        obj.final_receipt = new_doc
        obj.save()
    orders = InfirmaryOrder.objects.filter(infirmary = request.user.infirmary)
    return render (request,"users/get_infirmary_orders.html",{'requests':orders})

#@loggin_required
def delete_doc(request,doc_pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    MedicalDocuments.objects.get(pk=doc_pk).delete()
    return redirect('upload_medical_doc')


#@loggin_required
def payback(request,refund_pk):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    refund_request = InsuranceRefund.objects.get(pk = refund_pk)
    request.user.insurancecompany.wallet -= refund_request.refund_amount
    refund_request.patient.wallet+= refund_request.refund_amount
    request.user.insurancecompany.save()
    refund_request.patient.save()
    Transactions.objects.create(sender = request.user,receiver=refund_request.patient.user,amount=refund_request.refund_amount)
    InsuranceRefund.objects.get(pk=refund_pk).delete()
    return redirect('get_insurance_refund_requests')

def view_share_requests(request):
    emailsp = request.session["user"]
    request.user = User_Auth.objects.filter(email_id = emailsp)[0]
    if request.method=='POST' and "fulfil_req" in request.POST:
        form = RequestForm(request.POST)
        if form.is_valid():
            # form.save()
            # return redirect('share_docs')
            print(form.cleaned_data)
            document  = form.cleaned_data.get('document')
            req = form.cleaned_data.get('request')
            req.is_fulfilled  = True
            userhere  = req.patient.user
            ViewAccess.objects.create(document = document,  user=userhere)
            req.save()
            messages.success(request, f'Request fulfilled')
            


    # if request.method=='POST':
    #     val = "/media/profile_pics/q4.jpeg"
    #     docid = 1 
    #     print("i m here")
    #     h1 = ""
    #     with open(val , "rb") as f:
            
    #         encoded_string = base64.b64encode(f.read())
    #         print(encoded)
    #         h1 =  hashlib.sha256(encoded_string.encode()).hexdigest()
    #     request.session['hash'] = h1
    #     request.session['ids'] = ids
                    
    #     print(len(h1))            
    #     print(h1)
    #     print(type(h1))
    #     return redirect('upload_medical_doc')




    
    share_requests = DocRequestHospital.objects.filter(hospital=request.user.hospital, is_fulfilled = False)
    
    form2 = RequestForm()
    form2.fields['request'].queryset = share_requests
    form2.fields['document'].queryset = MedicalDocuments.objects.filter(owner=request.user , is_verified = True)

    return render (request,"users/view_share_requests.html",{'share_requests':share_requests ,  "form2" : form2})