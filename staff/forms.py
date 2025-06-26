from django import forms


    
# forms for Staff login
class StaffLoginForm(forms.Form):
    staffemail = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    staffpassword = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


#class StaffAnnouncement(forms.Form):
    #staffannouncement = forms.CharField(
        #label='Enter Announcement', max_length=50, required=True,
        #widget=forms.TextInput(
           # attrs={'class': 'form-control', 'placeholder': 'Enter your announcement here'})
   # )
