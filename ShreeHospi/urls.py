"""ShreeHospi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import re_path,include
from django.urls import path
from hospi import views as my_patient
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    re_path('admin/', admin.site.urls),
    re_path(r'^$', my_patient.index, name='home'),
    re_path(r'^patients$', my_patient.index, name='home'),
    re_path(r'^order/new/$', my_patient.new, name='new'),
    re_path(r'^(?P<patient_id>\d+)/ipd/$', my_patient.ipd, name='ipd'),
    re_path(r'^(?P<patient_id>\d+)/appointment/$', my_patient.createappointment, name='appointment'),
    re_path(r'^(?P<opd_id>\d+)/opdprint/$', my_patient.printopd, name='opd_print'),
    path('opdlist/', my_patient.opd_list,name='opdlist' ),
    path('ipdlist/', my_patient.ipd_list,name='ipdlist' ),
    path('update-patient/', my_patient.create_patient_record,name='create-patient-record' ),
    re_path(r'^(?P<ipd_id>\d+)/dischargedetails/$', my_patient.discharge_detail, name='discharge_details'),
    re_path(r'^(?P<ipd_id>\d+)/dischargeprint/$', my_patient.print, name='discharge_print'),
    path('dischargelist/', my_patient.discharge_list, name='discharge_list'),
    re_path(r'^(?P<ipd_id>\d+)/dischargehistory/$', my_patient.discharge_history, name='discharge_history'),
    re_path(r'^users/login/$', auth.LoginView.as_view, {'template_name': 'login.html'}, name='login'),
    re_path(r'^users/logout/$', auth.LogoutView.as_view, {'next_page': '/'}, name='logout'),

    re_path(r'^users/change_password/$', login_required(auth.PasswordResetForm), {'post_change_redirect' : '/','template_name': 'change_password.html'}, name='change_password'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

