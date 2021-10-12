from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Comment, Subject_categories, Test_files



class Login(forms.Form):
    username=forms.CharField(label='username', max_length=150)
    password=forms.CharField(widget=forms.PasswordInput())
class Register(UserCreationForm):
    class Meta:
        model=User
        fields=['email', 'username','password1', 'password2']
class Subject_Form(forms.Form):
    class Meta:
        model=Subject
        fields='__all__'
class Subject_categories_Form(forms.Form):
    class Meta:
        model = Subject_categories
        fields='__all__'
class Commentform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']

class TestFile(forms.ModelForm):
    class Meta:
        model=Test_files
        fields='__all__'
