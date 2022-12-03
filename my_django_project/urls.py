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
    path('login/',user_views.login,name="login"),
    path('profile/',user_views.profile,name="profile"),
    # path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name="logout"),
    path('', include('blog.urls')),
    path('verify/',user_views.verify_user,name='verify'),
    path('user_type/',user_views.get_user_type,name='user_type'),
    path('doc_share_otp/',user_views.doc_share_otp,name='doc_share_otp'),
    path('after_login/',user_views.after_login,name='after_login'),
     path('add_money/',user_views.add_money,name='add_money'),
    path('get_hospitals/',user_views.get_hospitals,name='get_hospitals'),
    path('get_shared_docs/',user_views.get_shared_docs,name='get_shared_docs'),
    path('share_docs/',user_views.share_docs,name='share_docs'),
    path('resetotp/',user_views.resetotp,name='resetotp'),


    path('view_share_requests/',user_views.view_share_requests,name='view_share_requests'),
    path('verifydoc/',user_views.verifydoc,name='verifydoc'),
    path('check/',user_views.check,name='check'),
    path('reset/',user_views.reset,name='reset'),
    path('sign/',user_views.sign,name='sign'),
    path('signI/',user_views.signI,name='signI'),
    path('get_infirmaries/',user_views.get_infirmaries,name='get_infirmaries'),
    path('get_insurancecompanies/',user_views.get_insurancecompanies,name='get_insurancecompanies'),
    path('upload_medical_doc/',user_views.upload_medical_doc,name='upload_medical_doc'), 
    path('ShareDocP/<str:pk>/',user_views.ShareDocP,name='ShareDocP'),
    path('place_infirmary_order/<str:inf_pk>/',user_views.place_infirmary_order,name='place_infirmary_order'),
    path('request_insurance_refund/<str:insurance_pk>/',user_views.request_insurance_refund,name='request_insurance_refund'),

    path('get_insurance_refund_requests/',user_views.get_insurance_refund_requests,name='get_insurance_refund_requests'),
    path('get_infirmary_orders/',user_views.get_infirmary_orders,name='get_infirmary_orders'),
    path('delete_doc/<str:doc_pk>/',user_views.delete_doc,name='delete_doc'),
    path('payback/<str:refund_pk>/',user_views.payback,name='payback'),
    path('media/profile_pics/<str:file>', user_views.media_access, name='media_access'),

    
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
