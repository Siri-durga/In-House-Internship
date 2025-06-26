from django import forms
from django.core.validators import MinValueValidator
from .models import AddTimeTable
from django.utils import timezone
from .models import AddStudent
from django.core.exceptions import ValidationError
from .models import Room




class AdminlogForm(forms.Form):
    adminemail = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    adminpassword = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class AddTimeTableForm(forms.ModelForm):
    class Meta:
        model = AddTimeTable
        fields = ['subject', 'iv_cse_a_faculty', 'iv_cse_b_faculty', 'iv_cse_c_faculty']


def all_emails():
    try:
        from .models import AddFaculty
        all_emails = [(i.email, i.email) for i in AddFaculty.objects.all()]
        return all_emails

    except:
        all_emails = ""
        return all_emails


branches = [
    ("cse", "Cse"),
    ("it", "It"),
    ("ece", "Ece")

]

semesters = [
    ("first", "First"),
    ("second", "Second")
]

year = [
    ("first", "First"),
    ("second", "Second"),
    ("third", "Third"),
    ("fourth", "Fourth")
]


subjects = [
    ('Select Subject', 'selects subject'),
    ('Probability and Statistics', 'probability and statistics'),

    ('Software Engineering', 'software engineering'),

    ('Databases', 'databases'),

    ('MEFA', 'MEFA'),


    ('Operating Systems', 'operating systems'),

    ('Database Lab ', 'database lab '),

    ('Full Stack Development',
        'Full Stack Development'),

    ('Operating systems lab ',
        'Operating systems lab '),

    ('Cognitive English lab', 'Cognitive English lab'),

]


class AddStudentForm(forms.Form):
    rollnumber = forms.CharField(
        label='Roll Number', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='Student Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        label='Department', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', max_length=100, required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    year = forms.IntegerField(
        label='Year', required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    semester = forms.IntegerField(
        label='Semester', required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    profile_url = forms.URLField(
        label='Profile URL', max_length=200, required=True,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )


    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File', 
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    




class AddexamhallForm(forms.Form):
    # ─── core exam-hall data ───────────────────────────────────────────────────
    Date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

    # 🔄 new subject fields
    subject1 = forms.CharField(
        label='Subject 1',
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Subject 1'}),
        required=True
    )
    subject2 = forms.CharField(
        label='Subject 2',
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Subject 2'}),
        required=False
    )

    noofrooms = forms.IntegerField(
        label="Rooms",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        validators=[MinValueValidator(1)],
        required=True
    )
    noofbenches = forms.IntegerField(
        label="No.of Benches per room",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        validators=[MinValueValidator(1)],
        required=True
    )

    rooms_list = forms.CharField(widget=forms.HiddenInput(), required=False)

    students_per_bench = forms.ChoiceField(
        label="Students per bench",
        choices=[(2, 'Two students per bench'), (3, 'Three students per bench')],
        widget=forms.RadioSelect(),
        required=True
    )

    # ─── dynamic room check-boxes added in __init__ ───────────────────────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rooms'] = forms.ModelMultipleChoiceField(
            queryset=Room.objects.all(),
            required=True,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            label="Select Rooms"
        )

    # ─── individual-field clean methods ───────────────────────────────────────
    def clean_Date(self):
        date = self.cleaned_data['Date']
        if date < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past.")
        return date

    def clean_noofrooms(self):
        val = self.cleaned_data['noofrooms']
        if val <= 0:
            raise forms.ValidationError("Number of rooms must be positive.")
        return val

    def clean_noofbenches(self):
        val = self.cleaned_data['noofbenches']
        if val <= 0:
            raise forms.ValidationError("Number of benches must be positive.")
        return val

    def clean_rooms(self):
        selected = self.cleaned_data.get('rooms', [])
        expected = self.cleaned_data.get('noofrooms') or 0
        if len(selected) != expected:
            raise forms.ValidationError(f"Please select exactly {expected} rooms.")
        return selected

    # ─── whole-form validation ────────────────────────────────────────────────
    def clean(self):
        cleaned = super().clean()

        noofrooms   = cleaned.get('noofrooms')
        noofbenches = cleaned.get('noofbenches')
        spp         = int(cleaned.get('students_per_bench', 2))

        if noofrooms and noofbenches:
            total_seats_available = noofrooms * noofbenches * spp
            total_students        = AddStudent.objects.count()
            if total_seats_available < total_students:
                raise forms.ValidationError(
                    "Not enough seats available for the total number of students.",
                    code='seats_unavailable'
                )
        return cleaned


class AddFacultyForm(forms.Form):

    name = forms.CharField(
        label='Faculty Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Faculty Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Faculty Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ChoiceField(
        label='Subject', choices=subjects, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    semester = forms.ChoiceField(
        label='Semester', choices=semesters, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.ChoiceField(
        label='Year', choices=year, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    #image = forms.ImageField(
       # label='Faculty Profile', required=True,
        #widget=forms.FileInput(attrs={'class': 'form-control'})
   # )


#class AdminAnnouncement(forms.Form):
 #   announcement = forms.CharField(
 #       label='Enter Announcement', max_length=150, required=True,
 #       widget=forms.TextInput(
 #           attrs={'class': 'form-control', 'placeholder': 'Enter your announcement here'})
 #   )
