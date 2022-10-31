import django_filters

from .models import *

class HospitalFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields =['fullname','location']

class InfirmaryFilter(django_filters.FilterSet):
    class Meta:
        model = Infirmary
        fields =['fullname','location']

class InsuranceCompanyFilter(django_filters.FilterSet):
    class Meta:
        model = InsuranceCompany
        fields =['fullname','location']