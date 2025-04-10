from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Tag

class CustomUserCreationForm(UserCreationForm):
    '''Custom form for user registration.'''

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

    def clean_username(self):
        '''Check if the username is already taken.'''
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username is already taken.")
        return username

    def clean_email(self):
        '''Check if the email is already taken.'''
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already taken.")
        return email

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.all(),
    widget=forms.CheckboxSelectMultiple,  # Display the tags as checkboxes
    required=False
    )
    class Meta:
        model = Task
        fields = ['title', 'priority', 'status', 'description', 'due_date', 'tags']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TagForm(forms.ModelForm):
    name = forms.CharField(required=False)
    class Meta:
        model = Tag
        fields = ['name']