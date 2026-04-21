from django import forms
from django.forms import ModelForm
from .models import *

class StudentForm(ModelForm):
    dob=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=Student.gender_choice,widget=forms.RadioSelect)
    address=forms.CharField(widget=forms.Textarea(attrs={'rows':4,'cols':40}))
    class Meta:
        model=Student
        fields='__all__'