from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date


class StudentForm(ModelForm):
    dob=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=Student.gender_choice)
    address=forms.CharField(widget=forms.Textarea(attrs={'rows':3,'cols':40}))
    class Meta:
        model=Student
        fields='__all__'

class CourseForm(ModelForm):
    class Meta:
        model=Course
        fields='__all__'

class EnrollmentForm(forms.ModelForm):

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']

        if start_date <= date.today():
            raise forms.ValidationError("Start date must be in the future!")

        return start_date
    start_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    
    class Meta:
        model = Enrollment
        exclude = ['student'] 

