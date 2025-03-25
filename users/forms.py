from django import forms
from django.contrib.auth.models import User
from .models import Profile, Project, Task, Comment
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        validators=[EmailValidator(message=('Invalid email address'))]
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
    #   Example of allowed domain lists
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address already registered.')

        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise ValidationError('Invalid email domain.')
        return email


class LoginForm(AuthenticationForm):
    """User login form"""
    class Meta:
        """The name of the form"""
        model = AuthenticationForm
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'role', 'image']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'end_date', 'team_member']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'project', 'assignee']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
