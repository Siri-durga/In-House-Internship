from django import forms


# forms for Student login
class StudentLoginForm(forms.Form):
    roll_number = forms.CharField(
        label='Roll Number', required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
