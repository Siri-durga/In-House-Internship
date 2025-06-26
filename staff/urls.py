from django.urls import path
from . import views

urlpatterns = [
    path('stafflogin', views.stafflogin, name="stafflogin"),
    path('viewstaffprofile', views.viewstaffprofile, name="viewstaffprofile"),
    #path('staffannouncement', views.staffannouncement, name="staffannouncement"),
    path('staffinvigilationschedule', views.staffinvigilationschedule,
         name="staffinvigilationschedule"),
    path('staffresetpassword', views.staffresetpassword, name="staffresetpassword"),
    path('updatestaffresetpassword', views.updatestaffresetpassword,
         name="updatestaffresetpassword"),






]
