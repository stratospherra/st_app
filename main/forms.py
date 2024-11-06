from django import forms
from django.contrib.auth.models import User
from .models import Student, Faculty, Speciality, StudentStatus



class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'email', 'phone', 'speciality', 'status', 'current_faculty', 'password']

    def save(self, commit=True):
        student = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['email'],  # Можно использовать email в качестве username
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        student.user = user
        if commit:
            student.save()
        return student

        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())



class UserSettingsForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.filter(is_active=True),
        widget=forms.Select,
        required=True,
        label="Select Faculty"
    )
    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.filter(is_active=True),
        widget=forms.Select,
        required=True,
        label="Select Speciality"
    )

    class Meta:
        model = Student
        fields = ['faculty', 'speciality']