from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Profile)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Infirmary)
admin.site.register(InsuranceCompany)
admin.site.register(MedicalDocuments)
admin.site.register(ViewAccess)
admin.site.register(User_Auth)
admin.site.register(InfirmaryOrder)
admin.site.register(InsuranceRefund)
admin.site.register(DocRequestHospital)
admin.site.register(Transactions)