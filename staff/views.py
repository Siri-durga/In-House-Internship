from django.shortcuts import render, redirect
from .forms import StaffLoginForm
from adminapp.models import AddFaculty, AdminAnnounce, AddTimeTable
from django.contrib import messages


# templates
STAFFLOGINPAGE = "stafflogin.html"
STAFFHOMEPAGE = "staffhome.html"
VIEWSTAFFPROFILEPAGE = "viewstaffprofile.html"
STAFFANNOUNCEMENTPAGE = "staffannouncement.html"
STAFFINVIGILATIONSCHEDULEPAGE = "staffinvigilationschedule.html"
STAFFRESETPASSWORDPAGE = "staffresetpassword.html"


# Writing function for staff Login


def stafflogin(req):
    context = {}
    context['form'] = StaffLoginForm()
    if req.method == "POST":
        form = StaffLoginForm(req.POST)
        if form.is_valid():
            staffemail = form.cleaned_data['staffemail']
            staffpassword = form.cleaned_data['staffpassword']
            print(staffemail, staffpassword)
            dc = AddFaculty.objects.filter(
                email=staffemail, password=staffpassword).exists()
            print(dc)
            if dc:
                req.session['staffemail'] = staffemail
                return render(req, STAFFHOMEPAGE)
            else:
                # Display error message for invalid credentials
                messages.error(req, 'Invalid email or password. Please try again.')
                print("Hello")
    return render(req, STAFFLOGINPAGE, context)


def viewstaffprofile(req):
    all_faculty = AddFaculty.objects.filter(email=req.session['staffemail'])
    return render(req, VIEWSTAFFPROFILEPAGE, {'all_faculty': all_faculty})


#def staffannouncement(req):
#    studentemail = req.session['staffemail']
#    all_messages = AdminAnnounce.objects.all()
 #   context = {}
 #   context['form'] = StaffAnnouncement()
 #   if req.method == "POST":
 #       form = StaffAnnouncement(req.POST)
 #       if form.is_valid():
 #           announcement = form.cleaned_data['staffannouncement']
 #           studentemail = req.session['staffemail']

  #          data = AdminAnnounce(
   #             announcement=announcement,
   #             senderemail=studentemail
   #         )
   #         data.save()
   #         return render(req, STAFFANNOUNCEMENTPAGE, {'form': StaffAnnouncement(), 'all_messages': all_messages, 'studentemail': studentemail})

   # return render(req, STAFFANNOUNCEMENTPAGE, {'form': StaffAnnouncement(), 'all_messages': all_messages, 'studentemail': studentemail})

def staffinvigilationschedule(req):
    dc = AddTimeTable.objects.all()
    print(dc)  # Check the output in your console
    return render(req, STAFFINVIGILATIONSCHEDULEPAGE, {'dc': dc})



def staffresetpassword(req):
    if req.method == "POST":
        old_password = req.POST['oldpassword']
        data = AddFaculty.objects.filter(
            email=req.session['staffemail'], password=old_password).exists()
        if data:
            return render(req, STAFFRESETPASSWORDPAGE, {'password': 'perfect'})
    return render(req, STAFFRESETPASSWORDPAGE, {'password': 'valid'})


def updatestaffresetpassword(req):
    if req.method == "POST":

        NewPassword = req.POST['NewPassword']
        ConfirmPassword = req.POST['ConfirmPassword']
        if NewPassword == ConfirmPassword:

            data = AddFaculty.objects.get(email=req.session['staffemail'])
            data.password = NewPassword
            data.save()
            return redirect("viewstaffprofile")
    return redirect("staffresetpassword")
