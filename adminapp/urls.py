from django.urls import path
from . import views
# Corrected import statement in adminapp.urls.py
from .models import AddTimeTable

urlpatterns = [
    path('', views.index, name="index"),
    path('adminlogin', views.adminlogin, name="adminlogin"),
    path('addstudents', views.addstudents, name="addstudents"),
    path('addexamhalls', views.addexamhalls, name="addexamhalls"),
    path('viewstudents', views.viewstudents, name="viewstudents"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('deletefaculty/<int:id>',views.deletefaculty,name="deletefaculty"),
    path('setseatallotment', views.setseatallotment, name="setseatallotment"),
    path('addfaculty', views.addfaculty, name="addfaculty"),
    path('viewfaculty', views.viewfaculty, name="viewfaculty"),
    #path('addannouncement', views.addannouncement, name="addannouncement"),
    path('addtimetable', views.addtimetable, name="addtimetable"),
    path('viewtimetable', views.viewtimetable, name="viewtimetable"),   
    path('viewallotedstudents',views.viewallotedstudents,name="viewallotedstudents"),
    path('download_details', views.download_details, name="download_details"),
    path('generate-pdf/', views.generate_examallotment_pdf, name='generate_pdf'),
    path('download_room_report/', views.download_room_report, name='download_room_report'),
    #path('attendance-sheet/<str:room_no>/', views.generate_attendance_sheet, name='attendance_sheet'),
    path('download-attendance-sheet/', views.attendance_sheet_home, name='download_attendance_sheet_home'),

]

