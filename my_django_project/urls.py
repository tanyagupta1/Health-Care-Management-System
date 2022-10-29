"""my_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name="register"),
    path('profile/',user_views.profile,name="profile"),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name="logout"),
    path('', include('blog.urls')),
    path('verify/',user_views.verify_user,name='verify'),
    path('user_type/',user_views.get_user_type,name='user_type'),
    path('doc_share_otp/',user_views.doc_share_otp,name='doc_share_otp'),
    path('after_login/',user_views.after_login,name='after_login'),
    path('get_hospitals/',user_views.get_hospitals,name='get_hospitals'),
    path('getDocsH/',user_views.getDocsH,name='getDocsH'),
    path('getDocsI/',user_views.getDocsI,name='getDocsI'),
    path('getDocsP/',user_views.getDocsP,name='getDocsP'),
    

    path('get_infirmaries/',user_views.get_infirmaries,name='get_infirmaries'),
    path('get_insurancecompanies/',user_views.get_insurancecompanies,name='get_insurancecompanies'),
    path('upload_medical_doc_p/',user_views.upload_medical_doc_p,name='upload_medical_doc_p'),
    path('upload_medical_doc_h/',user_views.upload_medical_doc_h,name='upload_medical_doc_h'), 
    path('ShareDocP/<str:pk>/',user_views.ShareDocP,name='ShareDocP')

    
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
