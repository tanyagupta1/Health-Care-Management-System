import django_filters

from .models import *

class HospitalFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields =['fullname','location']
