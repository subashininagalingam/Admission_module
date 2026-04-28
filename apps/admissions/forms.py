from django import forms
from .models import *
from datetime import date

class StudentForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = '__all__'


class AdmissionForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())


class EnrollmentForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date <= date.today():
            raise forms.ValidationError("Start date must be future!")
        return start_date

    class Meta:
        model = Enrollment
        fields = ['batch', 'start_date', 'payment_status']