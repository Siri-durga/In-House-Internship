from django.urls import path
from . import views

urlpatterns = [
    path('studentlogin', views.studentlogin, name="studentlogin"),
    path('viewstudentprofile', views.viewstudentprofile, name="viewstudentprofile"),
    #path('studentannouncement', views.studentannouncement,
         #name='studentannouncement'),
    path('studentexamdetails', views.studentexamdetails, name="studentexamdetails"),
    path('resetstudentpassword', views.resetstudentpassword,
         name='resetstudentpassword'),
    path('updateresetstudentpassword', views.updateresetstudentpassword,
         name="updateresetstudentpassword"),


]
