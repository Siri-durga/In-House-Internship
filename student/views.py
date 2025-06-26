from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentLoginForm
from adminapp.models import AddStudent, AdminAnnounce, Examallotment

# templates
STUDENTLOGINPAGE = "studentlogin.html"
STUDENTHOMEPAGE = "studenthome.html"
VIEWSTUDENTPROFILEPAGE = "viewstudentprofile.html"
STUDENTANNOUNCEMENTPAGE = "studentannouncement.html"
STUDENTEXAMDETAILSPAGE = "studentexamdetails.html"
RESETSTUDENTPASSWORDPAGE = "resetstudentpassword.html"
# Create your views here.



def studentlogin(req):
    context = {}
    context['form'] = StudentLoginForm()

    if req.method == "POST":
        form = StudentLoginForm(req.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            password = form.cleaned_data['password']
            # Check if a student with the provided roll number and password exists
            dc = AddStudent.objects.filter(rollnumber=roll_number, password=password).exists()
            if dc:
                req.session['student_roll_number'] = roll_number
                return render(req, STUDENTHOMEPAGE)
            else:
                # Display error message for invalid credentials
                messages.error(req, 'Invalid roll number or password. Please try again.')

    return render(req, STUDENTLOGINPAGE, context)


    
def viewstudentprofile(req):
    # Ensure user is authenticated before accessing the profile
    if 'student_roll_number' in req.session:
       roll_number = req.session['student_roll_number']
       student_profile = AddStudent.objects.filter(rollnumber=roll_number).first()
       if student_profile:
            #Pass the student_profile as a list to the template
            return render(req, VIEWSTUDENTPROFILEPAGE, {'student_profile': [student_profile]})
    # If user is not authenticated or profile doesn't exist, redirect to login
    return redirect('viewstudentprofile')

def studentannouncement(req):
    all_messages = AdminAnnounce.objects.all()
    return render(req, STUDENTANNOUNCEMENTPAGE, {'all_messages': all_messages})

def studentexamdetails(req):
    if 'student_roll_number' in req.session:
        roll_number = req.session['student_roll_number']
        data = Examallotment.objects.filter(Student_Id=roll_number)
        return render(req, STUDENTEXAMDETAILSPAGE, {'data': data})
    else:
        # Handle the case when the user is not authenticated
        return redirect('studentlogin')



def resetstudentpassword(req):
    if req.method == "POST":
        old_password = req.POST['oldpassword']
        # Retrieve the roll number from the session
        roll_number = req.session.get('student_roll_number')
        if roll_number:
            # Query the AddStudent model using the roll number
            data = AddStudent.objects.filter(rollnumber=roll_number, password=old_password).exists()
            if data:
                return render(req, RESETSTUDENTPASSWORDPAGE, {'password': 'perfect'})

    return render(req, RESETSTUDENTPASSWORDPAGE, {'password': 'valid'})


def updateresetstudentpassword(req):
    if req.method == "POST":
        NewPassword = req.POST['NewPassword']
        ConfirmPassword = req.POST['ConfirmPassword']

        if NewPassword == ConfirmPassword:
            # Retrieve the roll number from the session
            roll_number = req.session.get('student_roll_number')
            if roll_number:
                # Query the AddStudent model using the roll number
                student = AddStudent.objects.get(rollnumber=roll_number)
                student.password = NewPassword
                student.save()

    return redirect("viewstudentprofile")
