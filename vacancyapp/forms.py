from django import forms  
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User  
from .models import VacancyInfo, ApplicantInfo, EducationInfo 
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

class UserRegisterationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']


class ApplicantInfoForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Date picker
    issued_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Date picker
    
    class Meta:
        unique_together = ('user', 'applied_to') #Prevent duplicates application
        model = ApplicantInfo
        fields = ['first_name','last_name','dob','father_name','citizenship','issued_date','issued_district','mobile','profile_pic', 'upload_citizenship']
        

class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = EducationInfo
        fields = ['level','faculty','course_name','university_name','passed_year','grade_percent','upload_transcript1','upload_transcript2','upload_character','upload_license'
                  ,'upload_other','upload_other1']
        
      

class VacancyInfoForm(forms.ModelForm):
    class Meta:
        model = VacancyInfo 
        fields = ['vacancy_position','vacancy_group']

        # Create a formset for multiple applications
VacancyApplicationFormSet = modelformset_factory(
    VacancyInfo,
    form=VacancyInfoForm,
    extra=1,  # Prevents automatic empty forms
    can_delete=True,  # Allows users to delete a form if needed
)


