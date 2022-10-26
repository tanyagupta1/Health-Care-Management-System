from django.contrib import admin

# Register your models here.

from .models import Profile, Patient


admin.site.register(Profile)
admin.site.register(Patient)